"""Punto de entrada ASGI para Vercel (Python serverless).

Vercel detecta la variable `app` (ASGI) y la sirve. Mantener este archivo en la
raiz del proyecto para que el paquete `app/` sea importable.
"""
from app.main import app  # noqa: F401
