from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.calificaciones import CalificacionCreate, CalificacionResponse
from app.services.calificaciones import create_calificacion, get_calificacion, list_calificaciones
from app.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CalificacionResponse)
def create(calificacion: CalificacionCreate, db: Session = Depends(get_db)):
    return create_calificacion(db, calificacion)

@router.get("/{id_calificacion}", response_model=CalificacionResponse)
def get(id_calificacion: int, db: Session = Depends(get_db)):
    db_calificacion = get_calificacion(db, id_calificacion)
    if not db_calificacion:
        raise HTTPException(status_code=404, detail="Calificacion not found")
    return db_calificacion

@router.get("/", response_model=list[CalificacionResponse])
def list_all(db: Session = Depends(get_db)):
    return list_calificaciones(db)