# Changelog - Servicio de Calificaciones

## \[1.0.0] - 2025-06-09

### Agregado

* Creación del servicio de calificaciones.
* Endpoint **POST** `/calificaciones/` para agregar una nueva calificación.
* Endpoint **GET** `/calificaciones/{id_calificacion}` para obtener una calificación por su ID.
* Endpoint **GET** `/calificaciones/` para listar todas las calificaciones.
* Integración de modelos, esquemas y servicios con SQLAlchemy y Pydantic.
* Pruebas unitarias básicas para las operaciones CRUD de calificaciones.

## \[1.0.1] - 2025-06-09

### Corregido

* Validación de decimales en el campo `nota` para evitar errores de formato.

## [1.0.2] - 2025-06-10

### Agregado
- Se agrega el puerto 8003 al README.md
- Se agrega sección de documentación interactiva

### Corregido

- Se elimina FKs de modelo.

## [1.1.0] - 2025-07-02

### Agregado
- Endpoints adicionales:
  - **GET** `/calificaciones/por_estudiante/{id_estudiante}` para listar calificaciones por estudiante.
  - **GET** `/calificaciones/por_asignatura/{id_asignatura}` para listar calificaciones por asignatura.
- Validación externa de `id_estudiante` y `id_asignatura` contra APIs externas antes de registrar o consultar calificaciones.
- Servicio desacoplado para validaciones externas (`app/services/validaciones_externas.py`).
- Documentación Swagger enriquecida con `summary` y `description` en los endpoints.
- Actualización de la documentación complementaria en el `README.md` para reflejar los nuevos endpoints, validaciones y ejemplos de uso.
- Ejemplo de configuración de base de datos y ejecución en el `README.md`.

### Mejorado
- Refactorización de la arquitectura siguiendo principios SOFEA y buenas prácticas de desacoplamiento.
- Mejor organización de los servicios y routers.
- Ejemplos de respuesta y error más detallados en la documentación.

### Corregido
- Se asegura la correcta inicialización y conexión con la base de datos `calificaciones_db` usando SQLAlchemy y modelos sincronizados con la estructura real de la tabla.
- Se corrige la validación de existencia de estudiante y asignatura en todos los endpoints relevantes.

---
