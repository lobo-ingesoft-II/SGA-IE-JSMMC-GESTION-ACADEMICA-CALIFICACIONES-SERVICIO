from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.calificaciones import CalificacionCreate, CalificacionResponse
from app.services.calificaciones import create_calificacion, get_calificacion, list_calificaciones
from app.db import SessionLocal
from app.services.validaciones_externas import validar_estudiante, validar_asignatura
from app.services.calificaciones import (
    create_calificacion, get_calificacion, list_calificaciones,
    get_calificaciones_por_estudiante, get_calificaciones_por_asignatura
)
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

@router.get(
    "/por_estudiante/{id_estudiante}",
    response_model=list[CalificacionResponse],
    summary="Listar calificaciones por estudiante",
    description="Devuelve todas las calificaciones de un estudiante validando su existencia en el sistema externo."
)
def list_by_estudiante(id_estudiante: int, db: Session = Depends(get_db)):
    validar_estudiante(id_estudiante)
    return get_calificaciones_por_estudiante(db, id_estudiante)

@router.get(
    "/por_asignatura/{id_asignatura}",
    response_model=list[CalificacionResponse],
    summary="Listar calificaciones por asignatura",
    description="Devuelve todas las calificaciones de una asignatura validando su existencia en el sistema externo."
)
def list_by_asignatura(id_asignatura: int, db: Session = Depends(get_db)):
    validar_asignatura(id_asignatura)
    return get_calificaciones_por_asignatura(db, id_asignatura)