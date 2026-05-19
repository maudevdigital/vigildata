from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

EstadoIncidente = Literal["pendiente", "aprobado", "rechazado"]


class IncidenteCreate(BaseModel):
    tipo: str = Field(..., min_length=1, max_length=200)
    descripcion: str = Field(..., min_length=1)
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)
    comuna: str = Field(..., min_length=1, max_length=120)
    fecha: datetime = Field(
        ...,
        description="Instante del reporte (ISO 8601). Se guarda en BD como reloj naive en GMT-4.",
    )


class IncidenteResponse(BaseModel):
    id: int
    tipo: str
    descripcion: str
    fecha: datetime
    latitud: float
    longitud: float
    comuna: Optional[str] = None
    usuario_id: int

    model_config = {"from_attributes": True}

<<<<<<< Updated upstream
=======
class IncidenteEstadoUpdate(BaseModel):
    estado: EstadoIncidente = Field(..., description="pendiente | aprobado | rechazado")

>>>>>>> Stashed changes

class IncidenteFiltro(BaseModel):
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
