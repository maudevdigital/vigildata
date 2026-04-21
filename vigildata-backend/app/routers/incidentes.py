from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.incidente import Incidente
from app.models.usuario import Usuario
from app.schemas.incidente import IncidenteCreate, IncidenteResponse
from app.routers.auth import obtener_usuario_actual

router = APIRouter(prefix="/incidentes", tags=["incidentes"])


@router.post("/", response_model=IncidenteResponse, status_code=201)
def crear_incidente(
    data: IncidenteCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual),
):
    incidente = Incidente(**data.model_dump(), usuario_id=usuario.id)
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
