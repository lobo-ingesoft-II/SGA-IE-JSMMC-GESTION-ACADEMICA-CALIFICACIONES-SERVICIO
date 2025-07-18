from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import calificaciones
from app.db import init_db, test_connection

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from starlette.responses import Response
from app.routers.calificaciones import REQUEST_COUNT_CALIFICACIONES_ROUTERS, REQUEST_LATENCY_CALIFICACIONES_ROUTERS, ERROR_COUNT_CALIFICACIONES_ROUTERS


app = FastAPI(title="Calificaciones API")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React (puerto por defecto)
        "http://localhost:3001",  # React (puerto alternativo)
        "http://localhost:5173",  # Vite (puerto por defecto)
        "http://localhost:5174",  # Vite (puerto alternativo)
        "http://localhost:8080",  # Vue.js
        "http://localhost:4200",  # Angular
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:4200",
        # Agrega aquí la URL de tu frontend en producción
        # "https://tu-dominio-frontend.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    test_connection()

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception as e:
        status = 500
        raise e
    finally:
        latency = time.time() - start_time
        endpoint = request.url.path
        method = request.method

        REQUEST_COUNT_CALIFICACIONES_ROUTERS.labels(endpoint=endpoint, method=method).inc()
        REQUEST_LATENCY_CALIFICACIONES_ROUTERS.labels(endpoint=endpoint, method=method).observe(latency)


        
        if status >= 400: # type: ignore
            ERROR_COUNT_CALIFICACIONES_ROUTERS.labels(endpoint=endpoint, method=method, status_code=str(status)).inc() # type: ignore

    return response

# Registrar rutas
app.include_router(calificaciones.router, tags=["Calificaciones"])