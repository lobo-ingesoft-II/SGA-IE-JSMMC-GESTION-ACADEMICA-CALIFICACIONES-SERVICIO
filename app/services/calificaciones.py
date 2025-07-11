from sqlalchemy.orm import Session
from app.models.calificaciones import Calificacion
from app.services.validaciones_externas import validar_estudiante, validar_asignatura
from app.schemas.calificaciones import CalificacionCreate, CalificacionUpdate, CalificacionPartialUpdate  # Asegúrate de tener este esquema

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

def update_calificacion(db: Session, id_calificacion: int, calificacion: CalificacionUpdate):
    db_calificacion = db.query(Calificacion).filter(Calificacion.id_calificacion == id_calificacion).first()
    if not db_calificacion:
        return None
    db_calificacion.nota1 = calificacion.nota1 # type: ignore
    db_calificacion.nota2 = calificacion.nota2 # type: ignore
    db_calificacion.nota3 = calificacion.nota3 # type: ignore
    db_calificacion.observaciones = calificacion.observaciones # type: ignore
    db.commit()
    db.refresh(db_calificacion)
    return db_calificacion

def partial_update_calificacion(db: Session, id_calificacion: int, calificacion: CalificacionPartialUpdate):
    db_calificacion = db.query(Calificacion).filter(Calificacion.id_calificacion == id_calificacion).first()
    if not db_calificacion:
        return None
    update_data = calificacion.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_calificacion, field, value)
    db.commit()
    db.refresh(db_calificacion)
    return db_calificacion