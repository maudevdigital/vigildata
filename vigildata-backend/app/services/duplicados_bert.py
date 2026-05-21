"""HU-09 — Deteccion de denuncias repetidas con similitud semantica.

Usa sentence-transformers (modelo BERT multilingue) cuando esta disponible.
Si no esta instalado o falla la carga (entornos sin internet/CI), cae a un
embedding hashing deterministico que sirve para tests y desarrollo local.
"""
from __future__ import annotations

import hashlib
import math
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Iterable, Optional

from sqlalchemy.orm import Session

from app.models.incidente import Incidente

VENTANA_MINUTOS = int(os.getenv("HU09_VENTANA_MIN", "30"))
DISTANCIA_MAX_METROS = float(os.getenv("HU09_DISTANCIA_MAX_M", "200"))
UMBRAL_SIMILITUD = float(os.getenv("HU09_UMBRAL_SIMILITUD", "0.85"))
AUTO_APROBAR_DESDE = int(os.getenv("HU09_AUTO_APROBAR_DESDE", "3"))

_modelo_bert = None
_modelo_intento = False


def _cargar_bert():
    global _modelo_bert, _modelo_intento
    if _modelo_intento:
        return _modelo_bert
    _modelo_intento = True
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore

        _modelo_bert = SentenceTransformer(
            os.getenv("HU09_MODELO", "paraphrase-multilingual-MiniLM-L12-v2")
        )
    except Exception:
        _modelo_bert = None
    return _modelo_bert


_RE_PALABRA = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+")


def _embedding_hashing(texto: str, dim: int = 128) -> list[float]:
    """Fallback deterministico: bag-of-words con hashing trick + L2."""
    vec = [0.0] * dim
    for palabra in _RE_PALABRA.findall((texto or "").lower()):
        h = int(hashlib.md5(palabra.encode("utf-8")).hexdigest(), 16)
        vec[h % dim] += 1.0
    norma = math.sqrt(sum(v * v for v in vec))
    if norma > 0:
        vec = [v / norma for v in vec]
    return vec


def embed(texto: str) -> list[float]:
    modelo = _cargar_bert()
    if modelo is None:
        return _embedding_hashing(texto)
    vec = modelo.encode(texto or "", normalize_embeddings=True)
    return list(map(float, vec))


def similitud_coseno(a: Iterable[float], b: Iterable[float]) -> float:
    a = list(a)
    b = list(b)
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def distancia_metros(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine en metros."""
    R = 6_371_000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def encontrar_duplicado(db: Session, nuevo: Incidente) -> Optional[Incidente]:
    """Devuelve el incidente raiz si el `nuevo` es una repeticion segun reglas HU-09.

    Reglas:
      - Ventana temporal: ultimos VENTANA_MINUTOS minutos.
      - Misma comuna (cuando ambos la tienen).
      - Distancia <= DISTANCIA_MAX_METROS.
      - Similitud coseno entre embeddings de la descripcion >= UMBRAL_SIMILITUD.
    """
    desde = datetime.now(timezone.utc) - timedelta(minutes=VENTANA_MINUTOS)
    q = db.query(Incidente).filter(Incidente.fecha >= desde)
    if nuevo.comuna:
        q = q.filter(Incidente.comuna == nuevo.comuna)
    candidatos = q.all()
    if not candidatos:
        return None

    vec_nuevo = embed(nuevo.descripcion or "")
    mejor: Optional[Incidente] = None
    mejor_sim = 0.0
    for c in candidatos:
        if c.id and nuevo.id and c.id == nuevo.id:
            continue
        d = distancia_metros(nuevo.latitud, nuevo.longitud, c.latitud, c.longitud)
        if d > DISTANCIA_MAX_METROS:
            continue
        sim = similitud_coseno(vec_nuevo, embed(c.descripcion or ""))
        if sim >= UMBRAL_SIMILITUD and sim > mejor_sim:
            mejor = c
            mejor_sim = sim
    if mejor is None:
        return None
    # Retornar la raiz real (si el match ya estaba consolidado bajo otra)
    if mejor.incidente_raiz_id:
        raiz = db.query(Incidente).filter(Incidente.id == mejor.incidente_raiz_id).first()
        return raiz or mejor
    return mejor


def aplicar_consolidacion(db: Session, nuevo: Incidente, raiz: Incidente) -> bool:
    """Asocia `nuevo` a `raiz`. Si la raiz acumula >= AUTO_APROBAR_DESDE reportes,
    marca ambos como aprobados automaticamente. Devuelve True si fue auto-aprobado.
    """
    nuevo.incidente_raiz_id = raiz.id
    raiz.reportes_asociados = (raiz.reportes_asociados or 1) + 1
    if raiz.reportes_asociados >= AUTO_APROBAR_DESDE:
        raiz.estado = "aprobado"
        nuevo.estado = "aprobado"
        return True
    return False
