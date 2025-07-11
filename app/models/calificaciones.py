from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.db import Base

class Calificacion(Base):
    __tablename__ = "calificaciones"
    id_calificacion = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante = Column(Integer, nullable=False)
    id_asignatura = Column(Integer, nullable=False)
    periodo = Column(String(20), nullable=False)
    nota1 = Column(DECIMAL(4, 2), nullable=False)
    nota2 = Column(DECIMAL(4, 2), nullable=False)
    nota3 = Column(DECIMAL(4, 2), nullable=False)
    observaciones = Column(String(255))
    fecha_registro = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint('id_estudiante', 'id_asignatura', 'periodo', name='uq_calificacion'),
    )