import os
from dotenv import load_dotenv

load_dotenv()

# Caracteres a recortar de los valores de entorno: BOM, espacios y saltos de
# linea. Evita que un valor mal codificado (p.ej. cargado desde PowerShell con
# BOM/CRLF) rompa la app al parsear.
_BASURA = "﻿ \t\r\n"


def _clean(raw):
    if raw is None:
        return None
    return raw.strip(_BASURA)


def _int_env(name, default):
    val = _clean(os.getenv(name))
    if not val:
        return default
    try:
        return int(val)
    except ValueError:
        return default


DATABASE_URL = _clean(os.getenv("DATABASE_URL")) or "postgresql://user:password@localhost:5432/vigildata"
SECRET_KEY = _clean(os.getenv("SECRET_KEY")) or "dev-secret-key"
ALGORITHM = _clean(os.getenv("ALGORITHM")) or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = _int_env("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
