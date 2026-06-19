from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

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
        nivel_riesgo="alto",
    )

    # Aislamos la deteccion de duplicados (HU-09) para mantener una prueba
    # unitaria determinista: aqui solo validamos la persistencia del incidente.
    with patch.object(incidentes.duplicados_bert, "encontrar_duplicado", return_value=None):
        resultado = incidentes.crear_incidente(payload, db=db, usuario=usuario)

    db.add.assert_called_once_with(resultado)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(resultado)
    assert resultado.usuario_id == 12
    assert resultado.tipo == "Robo"
    assert resultado.comuna == "Santiago"
    assert resultado.nivel_riesgo == "alto"
    assert resultado.auto_aprobado is False


def test_listar_incidentes_sin_filtros_ordena_por_fecha_descendente():
    # query.filter se autorreferencia para poder seguir el encadenamiento de
    # filtros que aplica _aplicar_filtros.
    query = MagicMock()
    query.filter.return_value = query
    query.order_by.return_value.all.return_value = ["incidente-1", "incidente-2"]
    db = MagicMock()
    db.query.return_value = query

    resultado = incidentes.listar_incidentes(
        region=None,
        comuna=None,
        nivel_riesgo=None,
        estado=None,
        fecha_inicio=None,
        fecha_fin=None,
        db=db,
    )

    db.query.assert_called_once()
    # Aun sin filtros del usuario se aplican 2 filtros base:
    # 1) ocultar incidentes hijos (incidente_raiz_id == None)
    # 2) excluir rechazados (estado != "rechazado")
    assert query.filter.call_count == 2
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
        nivel_riesgo=None,
        estado=None,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        db=db,
    )

    assert resultado == []
    # 2 filtros base + comuna + fecha_inicio + fecha_fin = 5
    assert query.filter.call_count == 5
    query.order_by.assert_called_once()
