from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.calificaciones import Calificacion
from app.services.validaciones_externas import validar_estudiante, validar_asignatura
from app.schemas.calificaciones import CalificacionCreate, CalificacionUpdate, CalificacionPartialUpdate, CalificacionCreateForStudent, CalificacionUpdateForStudent

def create_calificacion(db: Session, calificacion: CalificacionCreate):
    try:
        validar_estudiante(calificacion.id_estudiante)
        validar_asignatura(calificacion.id_asignatura)
        db_calificacion = Calificacion(**calificacion.dict())
        db.add(db_calificacion)
        db.commit()
        db.refresh(db_calificacion)
        return db_calificacion
    except IntegrityError as e:
        db.rollback()
        if "uq_calificacion" in str(e) or "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=400, 
                detail=f"Ya existe una calificación para el estudiante {calificacion.id_estudiante} en la asignatura {calificacion.id_asignatura} para el periodo {calificacion.periodo}"
            )
        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

def create_calificacion_for_student(db: Session, id_estudiante: int, id_asignatura: int, calificacion: CalificacionCreateForStudent):
    """Crear o actualizar una calificación para un estudiante específico en una asignatura específica"""
    try:
        validar_estudiante(id_estudiante)
        validar_asignatura(id_asignatura)
        
        # Verificar si ya existe una calificación para este estudiante, asignatura y periodo
        existing_calificacion = db.query(Calificacion).filter(
            Calificacion.id_estudiante == id_estudiante,
            Calificacion.id_asignatura == id_asignatura,
            Calificacion.periodo == calificacion.periodo
        ).first()
        
        if existing_calificacion:
            # Actualizar la calificación existente
            existing_calificacion.nota1 = calificacion.nota1
            existing_calificacion.nota2 = calificacion.nota2
            existing_calificacion.nota3 = calificacion.nota3
            existing_calificacion.observaciones = calificacion.observaciones
            db.commit()
            db.refresh(existing_calificacion)
            return existing_calificacion
        else:
            # Crear nueva calificación
            db_calificacion = Calificacion(
                id_estudiante=id_estudiante,
                id_asignatura=id_asignatura,
                **calificacion.dict()
            )
            db.add(db_calificacion)
            db.commit()
            db.refresh(db_calificacion)
            return db_calificacion
            
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

def update_calificacion_for_student(db: Session, id_estudiante: int, id_asignatura: int, calificacion: CalificacionUpdateForStudent):
    """Actualizar solo las notas específicas de una calificación existente"""
    try:
        validar_estudiante(id_estudiante)
        validar_asignatura(id_asignatura)
        
        # Buscar la calificación existente
        existing_calificacion = db.query(Calificacion).filter(
            Calificacion.id_estudiante == id_estudiante,
            Calificacion.id_asignatura == id_asignatura,
            Calificacion.periodo == calificacion.periodo
        ).first()
        
        if not existing_calificacion:
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontró calificación para el estudiante {id_estudiante} en la asignatura {id_asignatura} para el periodo {calificacion.periodo}"
            )
        
        # Actualizar solo los campos que no son None
        update_data = calificacion.dict(exclude_unset=True, exclude={'periodo'})
        for field, value in update_data.items():
            if value is not None:
                setattr(existing_calificacion, field, value)
        
        db.commit()
        db.refresh(existing_calificacion)
        return existing_calificacion
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

def get_calificacion(db: Session, id_calificacion: int):
    return db.query(Calificacion).filter(Calificacion.id_calificacion == id_calificacion).first()

def list_calificaciones(db: Session):
    return db.query(Calificacion).all()

def get_calificaciones_por_estudiante(db: Session, id_estudiante: int):
    return db.query(Calificacion).filter(Calificacion.id_estudiante == id_estudiante).all()

def get_calificaciones_por_asignatura(db: Session, id_asignatura: int):
    return db.query(Calificacion).filter(Calificacion.id_asignatura == id_asignatura).all()

def get_calificaciones_por_estudiante_y_asignatura(db: Session, id_estudiante: int, id_asignatura: int):
    """Obtener calificaciones de un estudiante específico en una asignatura específica"""
    return db.query(Calificacion).filter(
        Calificacion.id_estudiante == id_estudiante,
        Calificacion.id_asignatura == id_asignatura
    ).all()

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