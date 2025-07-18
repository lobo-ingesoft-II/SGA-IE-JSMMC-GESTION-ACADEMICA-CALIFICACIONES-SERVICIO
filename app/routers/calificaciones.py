from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.schemas.calificaciones import CalificacionCreate, CalificacionResponse, CalificacionUpdate, CalificacionPartialUpdate, CalificacionCreateForStudent, CalificacionUpdateForStudent
from app.services.calificaciones import (
    create_calificacion,
    create_calificacion_for_student,
    update_calificacion_for_student,
    get_calificacion,
    list_calificaciones,
    get_calificaciones_por_estudiante,
    get_calificaciones_por_asignatura,
    get_calificaciones_por_estudiante_y_asignatura,
    update_calificacion,
    partial_update_calificacion,
)
from app.db import SessionLocal
from app.services.validaciones_externas import validar_estudiante, validar_asignatura
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from starlette.responses import Response
from prometheus_client import CollectorRegistry, generate_latest



router = APIRouter()

# Metricas 
REQUEST_COUNT_CALIFICACIONES_ROUTERS = Counter(
    "http_requests_total", 
    "TOTAL PETICIONES HTTP router-asignaturas",
    ["method", "endpoint"]
)

REQUEST_LATENCY_CALIFICACIONES_ROUTERS = Histogram(
    "http_request_duration_seconds", 
    "DURACION DE LAS PETICIONES router-asinaturas",
    ["method", "endpoint"],
    buckets=[0.1, 0.3, 1.0, 2.5, 5.0, 10.0]  
)

# 3. Errores por endpoint
ERROR_COUNT_CALIFICACIONES_ROUTERS = Counter(
    "http_request_errors_total",
    "TOTAL ERRORES HTTP (status >= 400)",
    ["endpoint", "method", "status_code"]
)
@router.get("/custom_metrics", tags=["Observabilidad"])
def custom_metrics():
    registry = CollectorRegistry()
    # Registrar métricas de asignaturas
    registry.register(REQUEST_COUNT_CALIFICACIONES_ROUTERS)
    registry.register(REQUEST_LATENCY_CALIFICACIONES_ROUTERS)
    registry.register(ERROR_COUNT_CALIFICACIONES_ROUTERS)
     
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CalificacionResponse)
def create(calificacion: CalificacionCreate, db: Session = Depends(get_db), request: Request = None):
    return create_calificacion(db, calificacion)

@router.post(
    "/estudiante/{id_estudiante}/asignatura/{id_asignatura}",
    response_model=CalificacionResponse,
    summary="Crear o actualizar calificación para estudiante en asignatura específica",
    description="Crea una nueva calificación o actualiza una existente para un estudiante específico en una asignatura específica. Si ya existe una calificación para el mismo periodo, se actualizarán las notas. Valida que tanto el estudiante como la asignatura existan en el sistema."
)
def create_for_student_and_subject(
    id_estudiante: int, 
    id_asignatura: int, 
    calificacion: CalificacionCreateForStudent, 
    db: Session = Depends(get_db),
    request: Request = None
):
    return create_calificacion_for_student(db, id_estudiante, id_asignatura, calificacion)

@router.patch(
    "/estudiante/{id_estudiante}/asignatura/{id_asignatura}",
    response_model=CalificacionResponse,
    summary="Actualizar notas específicas de un estudiante en una asignatura",
    description="Actualiza solo las notas específicas (nota1, nota2, nota3) que el profesor ha modificado para un estudiante en una asignatura y periodo específico. Perfecto para interfaces donde el profesor edita notas individuales en una tabla."
)
def update_student_grades(
    id_estudiante: int, 
    id_asignatura: int, 
    calificacion: CalificacionUpdateForStudent, 
    db: Session = Depends(get_db),
    request: Request = None
):
    return update_calificacion_for_student(db, id_estudiante, id_asignatura, calificacion)

@router.get("/{id_calificacion}", response_model=CalificacionResponse)
def get(id_calificacion: int, db: Session = Depends(get_db), request: Request = None):
    db_calificacion = get_calificacion(db, id_calificacion)
    if not db_calificacion:
        raise HTTPException(status_code=404, detail="Calificacion not found")
    return db_calificacion

@router.get("/", response_model=list[CalificacionResponse])
def list_all(db: Session = Depends(get_db), request: Request = None):
    return list_calificaciones(db)

@router.get(
    "/estudiante/{id_estudiante}/asignatura/{id_asignatura}",
    response_model=list[CalificacionResponse],
    summary="Obtener calificaciones de estudiante en asignatura específica",
    description="Devuelve todas las calificaciones de un estudiante específico en una asignatura específica. Valida que tanto el estudiante como la asignatura existan en el sistema."
)
def get_by_student_and_subject(
    id_estudiante: int, 
    id_asignatura: int, 
    db: Session = Depends(get_db),
    request: Request = None
):
    validar_estudiante(id_estudiante)
    validar_asignatura(id_asignatura)
    return get_calificaciones_por_estudiante_y_asignatura(db, id_estudiante, id_asignatura)

@router.get(
    "/por_estudiante/{id_estudiante}",
    response_model=list[CalificacionResponse],
    summary="Listar calificaciones por estudiante",
    description="Devuelve todas las calificaciones de un estudiante validando su existencia en el sistema externo."
)
def list_by_estudiante(id_estudiante: int, db: Session = Depends(get_db), request: Request = None):
    validar_estudiante(id_estudiante)
    return get_calificaciones_por_estudiante(db, id_estudiante)

@router.get(
    "/por_asignatura/{id_asignatura}",
    response_model=list[CalificacionResponse],
    summary="Listar calificaciones por asignatura",
    description="Devuelve todas las calificaciones de una asignatura validando su existencia en el sistema externo."
)
def list_by_asignatura(id_asignatura: int, db: Session = Depends(get_db), request: Request = None):
    validar_asignatura(id_asignatura)
    return get_calificaciones_por_asignatura(db, id_asignatura)

@router.put("/{id_calificacion}", response_model=CalificacionResponse)
def update(id_calificacion: int, calificacion: CalificacionUpdate, db: Session = Depends(get_db), request: Request = None):
    db_calificacion = update_calificacion(db, id_calificacion, calificacion)
    if not db_calificacion:
        raise HTTPException(status_code=404, detail="Calificacion not found")
    return db_calificacion

@router.patch("/{id_calificacion}", response_model=CalificacionResponse)
def partial_update(id_calificacion: int, calificacion: CalificacionPartialUpdate, db: Session = Depends(get_db), request: Request = None):
    db_calificacion = partial_update_calificacion(db, id_calificacion, calificacion)
    if not db_calificacion:
        raise HTTPException(status_code=404, detail="Calificacion not found")
    return db_calificacion

