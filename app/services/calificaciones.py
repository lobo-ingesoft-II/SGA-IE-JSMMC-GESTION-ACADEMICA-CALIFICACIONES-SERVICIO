from sqlalchemy.orm import Session
from app.models.calificaciones import Calificacion
from app.schemas.calificaciones import CalificacionCreate

def create_calificacion(db: Session, calificacion: CalificacionCreate):
    db_calificacion = Calificacion(**calificacion.dict())
    db.add(db_calificacion)
    db.commit()
    db.refresh(db_calificacion)
    return db_calificacion

def get_calificacion(db: Session, id_calificacion: int):
    return db.query(Calificacion).filter(Calificacion.id_calificacion == id_calificacion).first()

def list_calificaciones(db: Session):
    return db.query(Calificacion).all()