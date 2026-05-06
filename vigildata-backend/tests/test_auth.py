from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from pydantic import ValidationError

from app.config import ALGORITHM, SECRET_KEY
from app.models.usuario import Rol
from app.routers import auth
from app.schemas.usuario import UsuarioCreate


def _db_with_first(result):
    query = MagicMock()
    query.filter.return_value = query
    query.first.return_value = result

    db = MagicMock()
    db.query.return_value = query
    return db


def _usuario(id=1, email="persona@vigildata.cl", password="hash", rol=Rol.CIUDADANO):
    return SimpleNamespace(id=id, email=email, password=password, rol=rol)


def test_registro_crea_usuario_con_password_hasheada():
    db = _db_with_first(None)
    
    def mock_refresh(obj):
        obj.id = 1
        obj.rol = Rol.CIUDADANO
    db.refresh.side_effect = mock_refresh
    
    payload = UsuarioCreate(email="nuevo@vigildata.cl", password="secreto123")

    with patch.object(auth.pwd_context, "hash", return_value="hash-generado") as hash_mock:
        resultado = auth.registro(payload, db=db)

    hash_mock.assert_called_once_with("secreto123")
    db.add.assert_called_once()
    nuevo = db.add.call_args[0][0]
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(nuevo)
    assert nuevo.email == "nuevo@vigildata.cl"
    assert nuevo.password == "hash-generado"
    assert resultado.usuario.email == "nuevo@vigildata.cl"
    assert resultado.access_token is not None


def test_registro_rechaza_email_duplicado():
    db = _db_with_first(_usuario(email="existente@vigildata.cl"))
    payload = UsuarioCreate(email="existente@vigildata.cl", password="secreto123")

    with pytest.raises(HTTPException) as exc_info:
        auth.registro(payload, db=db)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "El email ya est\u00e1 registrado"
    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_login_exitoso_emite_token_y_usuario():
    usuario = _usuario(id=7, email="login@vigildata.cl", password="hash-db")
    db = _db_with_first(usuario)
    payload = UsuarioCreate(email="login@vigildata.cl", password="secreto123")

    with (
        patch.object(auth.pwd_context, "verify", return_value=True) as verify_mock,
        patch.object(auth, "crear_token", return_value="jwt-falso") as token_mock,
    ):
        resultado = auth.login(payload, db=db)

    verify_mock.assert_called_once_with("secreto123", "hash-db")
    token_mock.assert_called_once_with(
        {"sub": "7", "email": "login@vigildata.cl", "rol": "CIUDADANO"}
    )
    assert resultado.access_token == "jwt-falso"
    assert resultado.token_type == "bearer"
    assert resultado.usuario.email == "login@vigildata.cl"


@pytest.mark.parametrize("usuario_db, password_valida", [(None, False), (_usuario(), False)])
def test_login_rechaza_credenciales_invalidas(usuario_db, password_valida):
    db = _db_with_first(usuario_db)
    payload = UsuarioCreate(email="login@vigildata.cl", password="incorrecta")

    with patch.object(auth.pwd_context, "verify", return_value=password_valida):
        with pytest.raises(HTTPException) as exc_info:
            auth.login(payload, db=db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Credenciales inv\u00e1lidas"


def test_obtener_usuario_actual_decodifica_token_y_busca_usuario():
    usuario = _usuario(id=3)
    db = _db_with_first(usuario)
    token = auth.crear_token({"sub": "3"})
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    resultado = auth.obtener_usuario_actual(credentials=credentials, db=db)

    assert resultado is usuario
    db.query.assert_called_once()


def test_obtener_usuario_actual_rechaza_token_invalido():
    db = _db_with_first(None)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="no-es-jwt")

    with pytest.raises(HTTPException) as exc_info:
        auth.obtener_usuario_actual(credentials=credentials, db=db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Token inv\u00e1lido"


def test_obtener_usuario_actual_rechaza_usuario_inexistente():
    db = _db_with_first(None)
    token = jwt.encode({"sub": "404"}, SECRET_KEY, algorithm=ALGORITHM)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    with pytest.raises(HTTPException) as exc_info:
        auth.obtener_usuario_actual(credentials=credentials, db=db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Usuario no encontrado"


def test_usuario_create_valida_formato_email():
    with pytest.raises(ValidationError):
        UsuarioCreate(email="correo-invalido", password="secreto123")
