from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class IncidenteCreate(BaseModel):
    tipo: str
    descripcion: str
    latitud: float
    longitud: float
    region: Optional[str] = None
    comuna: Optional[str] = None


class IncidenteResponse(BaseModel):
    id: int
    tipo: str
    descripcion: str
    fecha: datetime
    latitud: float
    longitud: float
    region: Optional[str] = None
    comuna: Optional[str] = None
    usuario_id: int

    model_config = {"from_attributes": True}


class IncidenteFiltro(BaseModel):
    region: Optional[str] = None
    comuna: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
