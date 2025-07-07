from sqlalchemy.orm import Session
from app.models.calificaciones import Calificacion
from app.services.validaciones_externas import validar_estudiante, validar_asignatura
from app.schemas.calificaciones import CalificacionCreate  # Asegúrate de tener este esquema

def create_calificacion(db: Session, calificacion: CalificacionCreate):
    validar_estudiante(calificacion.id_estudiante)
    validar_asignatura(calificacion.id_asignatura)
    db_calificacion = Calificacion(**calificacion.dict())
    db.add(db_calificacion)
    db.commit()
    db.refresh(db_calificacion)
    return db_calificacion

def get_calificacion(db: Session, id_calificacion: int):
    return db.query(Calificacion).filter(Calificacion.id_calificacion == id_calificacion).first()

def list_calificaciones(db: Session):
    return db.query(Calificacion).all()

def get_calificaciones_por_estudiante(db: Session, id_estudiante: int):
    return db.query(Calificacion).filter(Calificacion.id_estudiante == id_estudiante).all()

def get_calificaciones_por_asignatura(db: Session, id_asignatura: int):
    return db.query(Calificacion).filter(Calificacion.id_asignatura == id_asignatura).all()