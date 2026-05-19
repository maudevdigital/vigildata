from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.incidente import Incidente
from app.models.usuario import Usuario, Rol
from app.schemas.incidente import IncidenteCreate, IncidenteResponse, IncidenteEstadoUpdate
from app.routers.auth import obtener_usuario_actual

router = APIRouter(prefix="/incidentes", tags=["incidentes"])


@router.post("/", response_model=IncidenteResponse, status_code=201)
def crear_incidente(
    data: IncidenteCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual),
):
    incidente = Incidente(**data.model_dump(exclude_none=True), usuario_id=usuario.id)
    db.add(incidente)
    db.commit()
    db.refresh(incidente)
    return incidente


@router.get("/", response_model=list[IncidenteResponse])
def listar_incidentes(
    region: Optional[str] = Query(None),
    comuna: Optional[str] = Query(None),
    nivel_riesgo: Optional[str] = Query(None),
    estado: Optional[str] = Query(None, description="Filtra por estado (pendiente, aprobado, rechazado, todos)"),
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Incidente)
    if estado == "todos":
        pass
    elif estado == "pendiente":
        # Se incluyen también aquellos creados antes que tengan estado nulo
        query = query.filter((Incidente.estado == "pendiente") | (Incidente.estado == None))
    elif estado:
        query = query.filter(Incidente.estado == estado)
    else:
        query = query.filter(Incidente.estado != "rechazado")

    if region:
        region_normalizada = region.strip()
        if region_normalizada:
            query = query.filter(func.lower(Incidente.region) == region_normalizada.lower())
    if comuna:
        comuna_normalizada = comuna.strip()
        if comuna_normalizada:
            query = query.filter(func.lower(Incidente.comuna) == comuna_normalizada.lower())
    if nivel_riesgo:
        query = query.filter(Incidente.nivel_riesgo == nivel_riesgo)
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


@router.patch("/{incidente_id}/estado", response_model=IncidenteResponse)
def cambiar_estado_incidente(
    incidente_id: int,
    data: IncidenteEstadoUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual),
):
    if usuario.rol.value != "ANALISTA":
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")
        
    if data.estado not in ["pendiente", "aprobado", "rechazado"]:
        raise HTTPException(status_code=400, detail="Estado inválido")
        
    incidente = db.query(Incidente).filter(Incidente.id == incidente_id).first()
    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
        
    incidente.estado = data.estado
    incidente.revisado_por_id = usuario.id
    incidente.fecha_revision = datetime.now()
    
    db.commit()
    db.refresh(incidente)
    return incidente
