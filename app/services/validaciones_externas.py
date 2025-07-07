import requests
from fastapi import HTTPException

ASIGNATURAS_API_URL = "http://127.0.0.1:8001/asignaturas/"
ESTUDIANTES_API_URL = "http://127.0.0.1:8005/estudiantes/"

def validar_asignatura(id_asignatura: int):
    resp = requests.get(f"{ASIGNATURAS_API_URL}{id_asignatura}")
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="La asignatura no existe")

def validar_estudiante(id_estudiante: int):
    resp = requests.get(f"{ESTUDIANTES_API_URL}{id_estudiante}")
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="El estudiante no existe")