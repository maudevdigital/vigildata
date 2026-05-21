"""HU-10 — Endpoint POST /auth/google.

Recibe `{id_token}` emitido por Google Identity Services en el frontend,
lo valida y devuelve un JWT propio (mismo formato que /auth/login).
Crea el usuario si no existe (rol CIUDADANO, provider='google') o lo vincula.
"""
from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario, Rol
from app.routers.auth import crear_token, pwd_context
from app.schemas.usuario import Token, UsuarioResponse
from app.services import google_oauth

router = APIRouter(prefix="/auth", tags=["auth"])


class GoogleLoginRequest(BaseModel):
    id_token: str


@router.post("/google", response_model=Token)
def login_google(body: GoogleLoginRequest, db: Session = Depends(get_db)):
    claims = google_oauth.verify_id_token(body.id_token)
    email = google_oauth.extraer_email(claims)

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        usuario = Usuario(
            email=email,
            password=pwd_context.hash(secrets.token_urlsafe(32)),
            rol=Rol.CIUDADANO,
            provider="supabase-google",
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
    else:
        # Vincular cuenta existente al provider Google la primera vez.
        if (usuario.provider or "local") == "local":
            usuario.provider = "supabase-google"
            db.commit()
            db.refresh(usuario)

    token = crear_token({
        "sub": str(usuario.id),
        "email": usuario.email,
        "rol": usuario.rol.value,
    })
    return Token(
        access_token=token,
        usuario=UsuarioResponse.model_validate(usuario),
    )
