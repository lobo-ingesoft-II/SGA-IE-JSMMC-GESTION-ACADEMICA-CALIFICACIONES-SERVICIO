from pydantic import BaseModel
from datetime import datetime

class CalificacionBase(BaseModel):
    id_estudiante: int
    id_asignatura: int
    periodo: str
    nota: float
    observaciones: str | None

class CalificacionCreate(CalificacionBase):
    pass

class CalificacionResponse(CalificacionBase):
    id_calificacion: int
    fecha_registro: datetime

    class Config:
        orm_mode = True