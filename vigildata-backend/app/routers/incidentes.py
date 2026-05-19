<<<<<<< Updated upstream
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
=======
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime, timezone
>>>>>>> Stashed changes
from typing import Optional

from app.database import get_db
from app.models.incidente import Incidente
<<<<<<< Updated upstream
from app.models.usuario import Usuario
from app.schemas.incidente import IncidenteCreate, IncidenteResponse
=======
from app.models.usuario import Usuario, Rol
from app.schemas.incidente import (
    IncidenteCreate,
    IncidenteResponse,
    IncidenteEstadoUpdate,
    IncidenteResumenResponse,
    ConteoItem,
)
>>>>>>> Stashed changes
from app.routers.auth import obtener_usuario_actual

router = APIRouter(prefix="/incidentes", tags=["incidentes"])

# Hora almacenada en BD como naive en este huso fijo (GMT-4 / UTC−4).
GMT_MINUS_4 = timezone(timedelta(hours=-4))


def _fecha_a_gmt4_naive(fecha: datetime) -> datetime:
    """Mismo instante, guardado como reloj local GMT-4 sin tzinfo (para la columna fecha)."""
    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=timezone.utc)
    return fecha.astimezone(GMT_MINUS_4).replace(tzinfo=None)


def _aplicar_filtros(
    query,
    *,
    region: Optional[str] = None,
    comuna: Optional[str] = None,
    nivel_riesgo: Optional[str] = None,
    estado: Optional[str] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
):
    if estado == "todos":
        pass
    elif estado == "pendiente":
        query = query.filter((Incidente.estado == "pendiente") | (Incidente.estado == None))
    elif estado:
        query = query.filter(Incidente.estado == estado)
    else:
        # Mapa y resumen público: solo incidentes aprobados por moderación
        query = query.filter(Incidente.estado == "aprobado")

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
    return query


@router.post("/", response_model=IncidenteResponse, status_code=201)
def crear_incidente(
    data: IncidenteCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual),
):
<<<<<<< Updated upstream
    fecha_bd = _fecha_a_gmt4_naive(data.fecha)
    payload = data.model_dump(exclude={"fecha"})
    incidente = Incidente(**payload, usuario_id=usuario.id, fecha=fecha_bd)
=======
    incidente = Incidente(
        **data.model_dump(exclude_none=True),
        usuario_id=usuario.id,
        estado="pendiente",
    )
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    query = db.query(Incidente)
    if comuna:
        query = query.filter(Incidente.comuna == comuna)
    if fecha_inicio:
        query = query.filter(Incidente.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Incidente.fecha <= fecha_fin)
    return query.order_by(Incidente.fecha.desc()).all()
=======
    query = _aplicar_filtros(
        db.query(Incidente),
        region=region,
        comuna=comuna,
        nivel_riesgo=nivel_riesgo,
        estado=estado,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )
    return query.order_by(Incidente.fecha.desc()).all()


@router.get("/resumen", response_model=IncidenteResumenResponse)
def resumen_incidentes(
    region: Optional[str] = Query(None),
    comuna: Optional[str] = Query(None),
    nivel_riesgo: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
):
    filtros = dict(
        region=region,
        comuna=comuna,
        nivel_riesgo=nivel_riesgo,
        estado=estado,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )

    base = _aplicar_filtros(db.query(Incidente), **filtros)
    total = base.count()

    comuna_etiqueta = func.coalesce(Incidente.comuna, "Sin comuna")
    por_comuna_rows = (
        _aplicar_filtros(
            db.query(comuna_etiqueta.label("etiqueta"), func.count(Incidente.id).label("total")),
            **filtros,
        )
        .group_by(comuna_etiqueta)
        .order_by(func.count(Incidente.id).desc())
        .all()
    )

    por_tipo_rows = (
        _aplicar_filtros(
            db.query(Incidente.tipo.label("etiqueta"), func.count(Incidente.id).label("total")),
            **filtros,
        )
        .group_by(Incidente.tipo)
        .order_by(func.count(Incidente.id).desc())
        .all()
    )

    return IncidenteResumenResponse(
        total=total,
        por_comuna=[ConteoItem(etiqueta=row.etiqueta, total=row.total) for row in por_comuna_rows],
        por_tipo=[ConteoItem(etiqueta=row.etiqueta, total=row.total) for row in por_tipo_rows],
    )


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
    incidente.fecha_revision = datetime.now(timezone.utc)

    db.commit()
    incidente = (
        db.query(Incidente)
        .options(joinedload(Incidente.revisador))
        .filter(Incidente.id == incidente_id)
        .first()
    )
    return incidente
>>>>>>> Stashed changes
