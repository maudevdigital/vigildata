"""HU-10 — Verificacion del access_token JWT emitido por Supabase Auth.

Soporta los dos esquemas de firma:
  - JWT Signing Keys nuevos (asimetrico ES256/RS256): se obtienen las claves
    publicas desde `<SUPABASE_URL>/auth/v1/.well-known/jwks.json` y se
    verifica la firma con la clave cuyo `kid` matchea el header del token.
  - Legacy JWT Secret (HS256): si `SUPABASE_JWT_SECRET` esta configurado se
    usa como fallback para tokens viejos.
"""
from __future__ import annotations

import json
import os
import time
from typing import Optional

import urllib.request
from fastapi import HTTPException
from jose import jwt, jwk, JWTError
from jose.utils import base64url_decode

_JWKS_CACHE: dict = {"ts": 0, "data": None}
_JWKS_TTL_SECONDS = 3600


def _jwks_url() -> Optional[str]:
    base = os.getenv("SUPABASE_URL", "").rstrip("/")
    if not base:
        return None
    return f"{base}/auth/v1/.well-known/jwks.json"


def _fetch_jwks() -> dict:
    url = _jwks_url()
    if not url:
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_URL no esta configurado en el backend",
        )
    now = time.time()
    if _JWKS_CACHE["data"] and now - _JWKS_CACHE["ts"] < _JWKS_TTL_SECONDS:
        return _JWKS_CACHE["data"]
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"No se pudo obtener JWKS: {exc}")
    _JWKS_CACHE["data"] = data
    _JWKS_CACHE["ts"] = now
    return data


def _verify_asimetrico(token: str) -> dict:
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    alg = headers.get("alg", "ES256")
    jwks = _fetch_jwks()
    key_dict = None
    for k in jwks.get("keys", []):
        if k.get("kid") == kid:
            key_dict = k
            break
    if not key_dict:
        raise HTTPException(status_code=401, detail=f"JWKS sin clave para kid={kid}")
    public_key = jwk.construct(key_dict, algorithm=alg)
    message, encoded_sig = token.rsplit(".", 1)
    decoded_sig = base64url_decode(encoded_sig.encode())
    if not public_key.verify(message.encode(), decoded_sig):
        raise HTTPException(status_code=401, detail="Firma JWT invalida")
    claims = jwt.get_unverified_claims(token)
    if claims.get("aud") not in (None, "authenticated"):
        raise HTTPException(status_code=401, detail="Audience invalido")
    exp = claims.get("exp")
    if exp and exp < time.time():
        raise HTTPException(status_code=401, detail="Token expirado")
    return claims


def _verify_hs256(token: str, secret: str) -> dict:
    try:
        return jwt.decode(token, secret, algorithms=["HS256"], audience="authenticated")
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=f"id_token invalido: {exc}")


def verify_id_token(id_token: str) -> dict:
    """Devuelve los claims si el access_token de Supabase es valido. Si no, 401."""
    if not id_token:
        raise HTTPException(status_code=401, detail="id_token vacio")
    try:
        headers = jwt.get_unverified_header(id_token)
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=f"id_token mal formado: {exc}")
    alg = headers.get("alg", "").upper()
    legacy_secret = os.getenv("SUPABASE_JWT_SECRET", "")
    if alg == "HS256" and legacy_secret:
        claims = _verify_hs256(id_token, legacy_secret)
    else:
        claims = _verify_asimetrico(id_token)
    if not claims.get("email"):
        raise HTTPException(status_code=401, detail="id_token sin email")
    return claims


def extraer_email(claims: dict) -> Optional[str]:
    return claims.get("email")
