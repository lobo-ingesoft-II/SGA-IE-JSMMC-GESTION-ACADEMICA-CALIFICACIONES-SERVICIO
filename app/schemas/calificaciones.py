from pydantic import BaseModel
from datetime import datetime

class CalificacionBase(BaseModel):
    id_estudiante: int
    id_asignatura: int
    periodo: str
    nota1: float
    nota2: float
    nota3: float
    observaciones: str | None = None

class CalificacionCreate(CalificacionBase):
    pass

class CalificacionUpdate(BaseModel):
    nota1: float
    nota2: float
    nota3: float
    observaciones: str | None = None

class CalificacionPartialUpdate(BaseModel):
    nota1: float | None = None
    nota2: float | None = None
    nota3: float | None = None
    observaciones: str | None = None

class CalificacionResponse(CalificacionBase):
    id_calificacion: int
    fecha_registro: datetime

    class Config:
        orm_mode = True