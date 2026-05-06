from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
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
    region: Optional[str] = Query(None),
    comuna: Optional[str] = Query(None),
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Incidente)
    if region:
        region_normalizada = region.strip()
        if region_normalizada:
            query = query.filter(func.lower(Incidente.region) == region_normalizada.lower())
    if comuna:
        comuna_normalizada = comuna.strip()
        if comuna_normalizada:
            query = query.filter(func.lower(Incidente.comuna) == comuna_normalizada.lower())
    if fecha_inicio:
        query = query.filter(Incidente.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Incidente.fecha <= fecha_fin)
    return query.order_by(Incidente.fecha.desc()).all()


@router.delete("/{incidente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_incidente(
    incidente_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual),
):
    if usuario.rol.value != "ANALISTA":
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")
        
    incidente = db.query(Incidente).filter(Incidente.id == incidente_id).first()
    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
        
    db.delete(incidente)
    db.commit()
    return None
