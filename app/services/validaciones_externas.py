import requests
from fastapi import HTTPException
import logging

ASIGNATURAS_API_URL = "http://sga-asignaturas-service:8001/asignaturas/"
ESTUDIANTES_API_URL = "http://sga-estudiantes-service:8005/estudiantes/"

def validar_asignatura(id_asignatura: int):
    try:
        resp = requests.get(f"{ASIGNATURAS_API_URL}{id_asignatura}", timeout=5)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="La asignatura no existe")
    except requests.exceptions.RequestException as e:
        logging.warning(f"No se pudo conectar al servicio de asignaturas: {e}")
        # Comentar la siguiente línea si quieres permitir crear calificaciones sin validación externa
        raise HTTPException(status_code=503, detail="Servicio de asignaturas no disponible")

def validar_estudiante(id_estudiante: int):
    try:
        resp = requests.get(f"{ESTUDIANTES_API_URL}{id_estudiante}", timeout=5)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="El estudiante no existe")
    except requests.exceptions.RequestException as e:
        logging.warning(f"No se pudo conectar al servicio de estudiantes: {e}")
        # Comentar la siguiente línea si quieres permitir crear calificaciones sin validación externa
        raise HTTPException(status_code=503, detail="Servicio de estudiantes no disponible")