from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Incidente(Base):
    __tablename__ = "incidentes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    fecha = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    region = Column(String, nullable=True)
    comuna = Column(String, nullable=True)
    nivel_riesgo = Column(String, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estado = Column(String, default="pendiente", nullable=False)
    revisado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_revision = Column(DateTime(timezone=True), nullable=True)
    incidente_raiz_id = Column(Integer, ForeignKey("incidentes.id"), nullable=True)
    reportes_asociados = Column(Integer, default=1, nullable=False)

    usuario = relationship("Usuario", foreign_keys=[usuario_id], back_populates="incidentes")
    revisador = relationship("Usuario", foreign_keys=[revisado_por_id])

    @property
    def revisado_por_email(self):
        return self.revisador.email if self.revisador else None
