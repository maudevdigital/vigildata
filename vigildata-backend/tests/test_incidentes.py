from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock

from app.routers import incidentes
from app.schemas.incidente import IncidenteCreate


def test_crear_incidente_persiste_usuario_autenticado():
    db = MagicMock()
    usuario = SimpleNamespace(id=12)
    payload = IncidenteCreate(
        tipo="Robo",
        descripcion="Robo de bicicleta",
        latitud=-33.4489,
        longitud=-70.6693,
        comuna="Santiago",
    )

    resultado = incidentes.crear_incidente(payload, db=db, usuario=usuario)

    db.add.assert_called_once_with(resultado)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(resultado)
    assert resultado.usuario_id == 12
    assert resultado.tipo == "Robo"
    assert resultado.comuna == "Santiago"


def test_listar_incidentes_sin_filtros_ordena_por_fecha_descendente():
    query = MagicMock()
    query.order_by.return_value.all.return_value = ["incidente-1", "incidente-2"]
    db = MagicMock()
    db.query.return_value = query

    resultado = incidentes.listar_incidentes(
        comuna=None,
        fecha_inicio=None,
        fecha_fin=None,
        db=db,
    )

    db.query.assert_called_once()
    query.filter.assert_not_called()
    query.order_by.assert_called_once()
    assert resultado == ["incidente-1", "incidente-2"]


def test_listar_incidentes_aplica_filtros_de_comuna_y_fechas():
    query = MagicMock()
    query.filter.return_value = query
    query.order_by.return_value.all.return_value = []
    db = MagicMock()
    db.query.return_value = query
    fecha_inicio = datetime(2026, 5, 1, tzinfo=timezone.utc)
    fecha_fin = datetime(2026, 5, 6, tzinfo=timezone.utc)

    resultado = incidentes.listar_incidentes(
        comuna="Santiago",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        db=db,
    )

    assert resultado == []
    assert query.filter.call_count == 3
    query.order_by.assert_called_once()
