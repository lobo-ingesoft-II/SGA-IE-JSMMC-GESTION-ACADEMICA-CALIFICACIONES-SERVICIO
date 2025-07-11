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

## [1.0.3] - 2025-07-02

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

## [1.0.4] - 2025-07-06

### Corregido
- Se hacen correciones a archivos: config.py, main.py, routers/calificaciones.py, services/calificaciones.py y validaciones_externas.py para realizar correctamente las operaciones del servicio y consultas a los otros servicios.

## [1.0.5] - 2025-07-11

### Agregado
- Se modifica el modelo y la tabla `calificaciones` para soportar tres notas (`nota1`, `nota2`, `nota3`) en vez de una sola.
- Se agrega restricción para que solo exista una calificación por estudiante, asignatura y periodo.
- Nuevos endpoints **PUT** y **PATCH** para actualización total y parcial de calificaciones.
- Nuevos esquemas Pydantic: `CalificacionUpdate` y `CalificacionPartialUpdate`.
- Nuevas funciones de servicio: `update_calificacion` y `partial_update_calificacion`.

### Mejorado
- Ajuste de los endpoints y servicios para trabajar con el nuevo modelo de calificaciones de tres notas.
- Actualización de los inserts de ejemplo y scripts SQL para reflejar la nueva estructura de la tabla `calificaciones`.
- Documentación actualizada en el `README.md` y en la documentación interactiva para reflejar los cambios en el modelo y los nuevos endpoints.

### Corregido
- Se corrigen errores en los scripts de migración de base de datos para soportar la nueva estructura de la tabla `calificaciones`.
- Se asegura la correcta validación y manejo de errores en los nuevos endpoints y funciones de actualización de calificaciones.
