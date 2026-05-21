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
    nivel_riesgo: str
    fecha: Optional[datetime] = None


class IncidenteResponse(BaseModel):
    id: int
    tipo: str
    descripcion: str
    fecha: datetime
    latitud: float
    longitud: float
    region: Optional[str] = None
    comuna: Optional[str] = None
    nivel_riesgo: Optional[str] = None
    usuario_id: int
    estado: str
    revisado_por_email: Optional[str] = None
    fecha_revision: Optional[datetime] = None
    incidente_raiz_id: Optional[int] = None
    reportes_asociados: int = 1
    auto_aprobado: bool = False

    model_config = {"from_attributes": True}

class IncidenteEstadoUpdate(BaseModel):
    estado: str


class IncidenteFiltro(BaseModel):
    region: Optional[str] = None
    comuna: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None


class ConteoItem(BaseModel):
    etiqueta: str
    total: int


class IncidenteResumenResponse(BaseModel):
    total: int
    por_comuna: list[ConteoItem]
    por_tipo: list[ConteoItem]
