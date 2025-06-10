from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.sql import func
from app.db import Base

class Calificacion(Base):
    __tablename__ = "calificaciones"

    id_calificacion = Column(Integer, primary_key=True, index=True)
    id_estudiante = Column(Integer, nullable=False)
    id_asignatura = Column(Integer, nullable=False)
    periodo = Column(String(20), nullable=False)
    nota = Column(Numeric(4, 2), nullable=False)
    observaciones = Column(String(255), nullable=True)
    fecha_registro = Column(DateTime, nullable=False, default=func.now())