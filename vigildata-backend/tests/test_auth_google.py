"""HU-10 — tests del endpoint POST /auth/google."""
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import incidente as _i  # noqa
from app.models import usuario as _u  # noqa
from app.models.usuario import Usuario


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    def _override():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_google_login_crea_usuario_ciudadano_nuevo(client):
    fake_claims = {
        "iss": "https://xxxxx.supabase.co/auth/v1",
        "aud": "authenticated",
        "email": "nuevo@gmail.com",
        "email_verified": True,
        "sub": "00000000-0000-0000-0000-000000000001",
        "app_metadata": {"provider": "google"},
    }
    with patch("app.services.google_oauth.verify_id_token", return_value=fake_claims):
        r = client.post("/auth/google", json={"id_token": "fake-token"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["usuario"]["email"] == "nuevo@gmail.com"
    assert data["usuario"]["rol"] == "CIUDADANO"
    assert data["access_token"]


def test_google_login_vincula_cuenta_existente(client):
    # Pre-creo un usuario local con el mismo email
    fake_claims = {
        "aud": "authenticated",
        "email": "existente@gmail.com",
        "app_metadata": {"provider": "google"},
    }
    # Primer login -> crea
    with patch("app.services.google_oauth.verify_id_token", return_value=fake_claims):
        r1 = client.post("/auth/google", json={"id_token": "t1"})
    assert r1.status_code == 200
    # Segundo login -> mismo id, no duplica
    with patch("app.services.google_oauth.verify_id_token", return_value=fake_claims):
        r2 = client.post("/auth/google", json={"id_token": "t2"})
    assert r2.status_code == 200
    assert r1.json()["usuario"]["id"] == r2.json()["usuario"]["id"]


def test_google_login_id_token_invalido_devuelve_401(client):
    from fastapi import HTTPException

    def _raise(*_a, **_k):
        raise HTTPException(status_code=401, detail="id_token invalido")

    with patch("app.services.google_oauth.verify_id_token", side_effect=_raise):
        r = client.post("/auth/google", json={"id_token": "bad"})
    assert r.status_code == 401
