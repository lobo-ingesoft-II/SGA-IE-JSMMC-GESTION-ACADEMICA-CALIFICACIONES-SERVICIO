import requests
from fastapi import HTTPException

ESTUDIANTES_API_URL = "http://estudiantes_api/estudiantes/"
ASIGNATURAS_API_URL = "http://asignaturas_api/asignaturas/"

def validar_estudiante(id_estudiante: int):
    resp = requests.get(f"{ESTUDIANTES_API_URL}{id_estudiante}")
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="El estudiante no existe")

def validar_asignatura(id_asignatura: int):
    resp = requests.get(f"{ASIGNATURAS_API_URL}{id_asignatura}")
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="La asignatura no existe")