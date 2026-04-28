from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from app.database import Base

_GMT_MINUS_4 = timezone(timedelta(hours=-4))


def _default_fecha_gmt4_naive() -> datetime:
    return datetime.now(timezone.utc).astimezone(_GMT_MINUS_4).replace(tzinfo=None)


class Incidente(Base):
    __tablename__ = "incidentes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    fecha = Column(DateTime, default=_default_fecha_gmt4_naive, nullable=False)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    comuna = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="incidentes")
