from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.routers import incidentes
from app.schemas.incidente import IncidenteCreate, IncidenteEstadoUpdate


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
        region=None,
        comuna=None,
        fecha_inicio=None,
        fecha_fin=None,
        db=db,
    )

    db.query.assert_called_once()
    query.filter.assert_called_once()
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
        region=None,
        comuna="Santiago",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        db=db,
    )

    assert resultado == []
    assert query.filter.call_count == 4
    query.order_by.assert_called_once()


def test_resumen_incidentes_agrupa_por_comuna_y_tipo():
    base_query = MagicMock()
    base_query.count.return_value = 5

    comuna_query = MagicMock()
    comuna_query.filter.return_value = comuna_query
    comuna_query.group_by.return_value = comuna_query
    comuna_query.order_by.return_value = comuna_query
    comuna_query.all.return_value = [
        SimpleNamespace(etiqueta="Santiago", total=3),
        SimpleNamespace(etiqueta="Providencia", total=2),
    ]

    tipo_query = MagicMock()
    tipo_query.filter.return_value = tipo_query
    tipo_query.group_by.return_value = tipo_query
    tipo_query.order_by.return_value = tipo_query
    tipo_query.all.return_value = [
        SimpleNamespace(etiqueta="Robo", total=4),
        SimpleNamespace(etiqueta="Asalto", total=1),
    ]

    db = MagicMock()
    db.query.side_effect = [base_query, comuna_query, tipo_query]

    resultado = incidentes.resumen_incidentes(
        region=None,
        comuna="Santiago",
        nivel_riesgo=None,
        estado=None,
        fecha_inicio=None,
        fecha_fin=None,
        db=db,
    )

    assert resultado.total == 5
    assert resultado.por_comuna[0].etiqueta == "Santiago"
    assert resultado.por_comuna[0].total == 3
    assert resultado.por_tipo[0].etiqueta == "Robo"
    assert resultado.por_tipo[0].total == 4
    assert db.query.call_count == 3


def test_cambiar_estado_requiere_rol_analista():
    usuario = SimpleNamespace(id=1, rol=SimpleNamespace(value="CIUDADANO"))
    db = MagicMock()

    with pytest.raises(HTTPException) as exc_info:
        incidentes.cambiar_estado_incidente(
            1,
            IncidenteEstadoUpdate(estado="aprobado"),
            db=db,
            usuario=usuario,
        )

    assert exc_info.value.status_code == 403


def test_cambiar_estado_registra_revisor_y_fecha():
    incidente = SimpleNamespace(
        id=5,
        estado="pendiente",
        revisado_por_id=None,
        fecha_revision=None,
        revisador=None,
    )
    query = MagicMock()
    query.filter.return_value = query
    query.options.return_value = query
    query.first.side_effect = [incidente, incidente]

    db = MagicMock()
    db.query.return_value = query
    analista = SimpleNamespace(id=2, rol=SimpleNamespace(value="ANALISTA"))

    with patch.object(incidentes, "datetime") as dt_mock:
        ahora = datetime(2026, 5, 19, 12, 0, tzinfo=timezone.utc)
        dt_mock.now.return_value = ahora
        resultado = incidentes.cambiar_estado_incidente(
            5,
            IncidenteEstadoUpdate(estado="aprobado"),
            db=db,
            usuario=analista,
        )

    assert resultado.estado == "aprobado"
    assert resultado.revisado_por_id == 2
    assert resultado.fecha_revision == ahora
    db.commit.assert_called_once()
