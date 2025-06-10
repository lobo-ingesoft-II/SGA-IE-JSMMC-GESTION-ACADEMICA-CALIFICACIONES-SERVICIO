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