"""from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "calificaciones_http_requests_total",
    "Total de peticiones HTTP en calificaciones",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "calificaciones_http_request_duration_seconds",
    "Duración de las peticiones HTTP en calificaciones",
    ["method", "endpoint"],
    buckets=[0.1, 0.3, 1.0, 2.5, 5.0, 10.0]
)

ERROR_COUNT = Counter(
    "calificaciones_http_request_errors_total",
    "Total de errores HTTP (status >= 400) en calificaciones",
    ["endpoint", "method", "status_code"]
)

def prometheus_metrics(endpoint_name):
    import time
    from fastapi import Request, HTTPException
    from starlette.requests import Request as StarletteRequest
    import inspect

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Intentar obtener el objeto Request de kwargs
            request: Request | None = kwargs.get("request")

            # Si no está en kwargs, buscarlo en args por tipo
            if request is None:
                for arg in args:
                    if isinstance(arg, (Request, StarletteRequest)):
                        request = arg
                        break

            method = request.method if request else "N/A"
            start_time = time.time()

            try:
                REQUEST_COUNT.labels(method=method, endpoint=endpoint_name).inc()
                response = await func(*args, **kwargs)
                REQUEST_LATENCY.labels(method=method, endpoint=endpoint_name).observe(time.time() - start_time)
                return response
            except HTTPException as e:
                ERROR_COUNT.labels(endpoint=endpoint_name, method=method, status_code=e.status_code).inc()
                REQUEST_LATENCY.labels(method=method, endpoint=endpoint_name).observe(time.time() - start_time)
                raise
        return wrapper
    return decorator """
from prometheus_client import Counter, Histogram
from fastapi import Request, HTTPException
from functools import wraps
import time

REQUEST_COUNT = Counter(
    "asistencia_http_requests_total",
    "Total de peticiones HTTP en asistencia",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "asistencia_http_request_duration_seconds",
    "Duración de las peticiones HTTP en asistencia",
    ["method", "endpoint"],
    buckets=[0.1, 0.3, 1.0, 2.5, 5.0, 10.0]
)

ERROR_COUNT = Counter(
    "asistencia_http_request_errors_total",
    "Total de errores HTTP (status >= 400) en asistencia",
    ["endpoint", "method", "status_code"]
)

def prometheus_metrics(endpoint_name):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Buscar instancia de Request en *args
            request = next((arg for arg in args if isinstance(arg, Request)), None)
            method = request.method if request else "N/A"
            start_time = time.time()
            try:
                REQUEST_COUNT.labels(method=method, endpoint=endpoint_name).inc()
                response = await func(*args, **kwargs)
                REQUEST_LATENCY.labels(method=method, endpoint=endpoint_name).observe(time.time() - start_time)
                return response
            except HTTPException as e:
                ERROR_COUNT.labels(endpoint=endpoint_name, method=method, status_code=e.status_code).inc()
                REQUEST_LATENCY.labels(method=method, endpoint=endpoint_name).observe(time.time() - start_time)
                raise
        return wrapper
    return decorator

