from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.database import get_db
from app.models.incidente import Incidente
from app.models.usuario import Usuario
from app.schemas.incidente import IncidenteCreate, IncidenteResponse
from app.routers.auth import obtener_usuario_actual

router = APIRouter(prefix="/incidentes", tags=["incidentes"])

# Hora almacenada en BD como naive en este huso fijo (GMT-4 / UTC−4).
GMT_MINUS_4 = timezone(timedelta(hours=-4))


def _fecha_a_gmt4_naive(fecha: datetime) -> datetime:
    """Mismo instante, guardado como reloj local GMT-4 sin tzinfo (para la columna fecha)."""
    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=timezone.utc)
    return fecha.astimezone(GMT_MINUS_4).replace(tzinfo=None)


@router.post("/", response_model=IncidenteResponse, status_code=201)
def crear_incidente(
    data: IncidenteCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual),
):
    fecha_bd = _fecha_a_gmt4_naive(data.fecha)
    payload = data.model_dump(exclude={"fecha"})
    incidente = Incidente(**payload, usuario_id=usuario.id, fecha=fecha_bd)
    db.add(incidente)
    db.commit()
    db.refresh(incidente)
    return incidente


@router.get("/", response_model=list[IncidenteResponse])
def listar_incidentes(
    comuna: Optional[str] = Query(None),
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Incidente)
    if comuna:
        query = query.filter(Incidente.comuna == comuna)
    if fecha_inicio:
        query = query.filter(Incidente.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Incidente.fecha <= fecha_fin)
    return query.order_by(Incidente.fecha.desc()).all()
