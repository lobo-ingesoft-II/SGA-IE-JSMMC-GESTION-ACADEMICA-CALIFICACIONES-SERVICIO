from fastapi import FastAPI
from app.routers import calificaciones
from app.db import init_db, test_connection

app = FastAPI(title="Calificaciones API")

@app.on_event("startup")
def startup_event():
    init_db()
    test_connection()

# Registrar rutas
app.include_router(calificaciones.router, prefix="/calificaciones", tags=["Calificaciones"])