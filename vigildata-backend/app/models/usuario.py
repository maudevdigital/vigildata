from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class Rol(str, enum.Enum):
    CIUDADANO = "CIUDADANO"
    ANALISTA = "ANALISTA"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(SAEnum(Rol), default=Rol.CIUDADANO, nullable=False)
    provider = Column(String, default="local", nullable=False)

    incidentes = relationship(
        "Incidente",
        back_populates="usuario",
        foreign_keys="Incidente.usuario_id",
    )
