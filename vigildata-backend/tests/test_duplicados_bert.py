"""HU-09 — tests del servicio de deteccion de duplicados con BERT.

Estos tests usan una BD SQLite in-memory aislada para verificar reglas:
- ventana temporal de 30 min
- distancia <= 200 m y misma comuna
- umbral de similitud >= 0.85
- auto-aprobacion cuando hay >= 3 reportes asociados.
"""
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import incidente as _i  # noqa: registra modelo
from app.models import usuario as _u  # noqa
from app.models.incidente import Incidente
from app.models.usuario import Usuario
from app.services import duplicados_bert


@pytest.fixture()
def db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    s.add(Usuario(email="ciudadano@test.cl", password="x"))
    s.commit()
    try:
        yield s
    finally:
        s.close()


def _incidente(db, descripcion, lat=-33.4489, lon=-70.6693, comuna="Santiago", minutos_atras=0):
    inc = Incidente(
        tipo="Robo",
        descripcion=descripcion,
        latitud=lat,
        longitud=lon,
        comuna=comuna,
        nivel_riesgo="Medio",
        usuario_id=1,
        fecha=datetime.now(timezone.utc) - timedelta(minutes=minutos_atras),
    )
    db.add(inc)
    db.commit()
    db.refresh(inc)
    return inc


def test_similitud_coseno_simetria_y_normalizacion():
    a = duplicados_bert.embed("robo de bicicleta en la plaza")
    b = duplicados_bert.embed("robo de bicicleta en la plaza")
    assert duplicados_bert.similitud_coseno(a, b) == pytest.approx(1.0, abs=1e-6)


def test_distancia_metros_haversine_misma_ubicacion_es_cero():
    assert duplicados_bert.distancia_metros(-33.45, -70.66, -33.45, -70.66) == pytest.approx(0.0, abs=1e-3)


def test_distancia_metros_200m_aproximado():
    # ~200 m al norte
    d = duplicados_bert.distancia_metros(-33.4489, -70.6693, -33.4471, -70.6693)
    assert 180 < d < 230


def test_duplicado_detecta_descripciones_similares_cercanas(db):
    raiz = _incidente(db, "Robo de bicicleta en la plaza principal")
    nuevo = Incidente(
        tipo="Robo",
        descripcion="Robo de bicicleta en la plaza principal",
        latitud=-33.4489,
        longitud=-70.6693,
        comuna="Santiago",
        nivel_riesgo="Medio",
        usuario_id=1,
        fecha=datetime.now(timezone.utc),
    )
    match = duplicados_bert.encontrar_duplicado(db, nuevo)
    assert match is not None
    assert match.id == raiz.id


def test_duplicado_descarta_si_estan_lejos(db):
    _incidente(db, "Robo de bicicleta en la plaza", lat=-33.4489, lon=-70.6693)
    nuevo = Incidente(
        tipo="Robo",
        descripcion="Robo de bicicleta en la plaza",
        latitud=-33.5000,  # > 1 km
        longitud=-70.6693,
        comuna="Santiago",
        nivel_riesgo="Medio",
        usuario_id=1,
        fecha=datetime.now(timezone.utc),
    )
    assert duplicados_bert.encontrar_duplicado(db, nuevo) is None


def test_duplicado_descarta_si_paso_mas_de_30_min(db):
    _incidente(db, "Robo de bicicleta en la plaza", minutos_atras=45)
    nuevo = Incidente(
        tipo="Robo",
        descripcion="Robo de bicicleta en la plaza",
        latitud=-33.4489,
        longitud=-70.6693,
        comuna="Santiago",
        nivel_riesgo="Medio",
        usuario_id=1,
        fecha=datetime.now(timezone.utc),
    )
    assert duplicados_bert.encontrar_duplicado(db, nuevo) is None


def test_auto_aprueba_al_llegar_al_tercer_reporte(db):
    raiz = _incidente(db, "Robo con violencia en la esquina del banco")
    # Asocio dos reportes consecutivos -> raiz queda con reportes_asociados = 3 al tercer match
    for _ in range(2):
        nuevo = Incidente(
            tipo="Robo",
            descripcion="Robo con violencia en la esquina del banco",
            latitud=-33.4489,
            longitud=-70.6693,
            comuna="Santiago",
            nivel_riesgo="Medio",
            usuario_id=1,
            fecha=datetime.now(timezone.utc),
        )
        db.add(nuevo)
        db.flush()
        match = duplicados_bert.encontrar_duplicado(db, nuevo)
        duplicados_bert.aplicar_consolidacion(db, nuevo, match)
        db.commit()
    # Tercer reporte equivalente
    tercero = Incidente(
        tipo="Robo",
        descripcion="Robo con violencia en la esquina del banco",
        latitud=-33.4489,
        longitud=-70.6693,
        comuna="Santiago",
        nivel_riesgo="Medio",
        usuario_id=1,
        fecha=datetime.now(timezone.utc),
    )
    db.add(tercero)
    db.flush()
    match = duplicados_bert.encontrar_duplicado(db, tercero)
    auto = duplicados_bert.aplicar_consolidacion(db, tercero, match)
    db.commit()
    db.refresh(raiz)
    assert auto is True
    assert raiz.estado == "aprobado"
    assert raiz.reportes_asociados >= 3
