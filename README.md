# Servicio de Calificaciones

## Descripción

Este servicio permite gestionar las calificaciones de los estudiantes en el sistema académico. Proporciona funcionalidades para crear, obtener y listar calificaciones, permitiendo un seguimiento detallado del desempeño estudiantil.

## Endpoints

### Crear una calificación

**POST** `/calificaciones/`

#### Request Body

```json
{
  "id_estudiante": 1,
  "id_asignatura": 1,
  "periodo": "2025-1",
  "nota": 4.5,
  "observaciones": "Excelente rendimiento"
}
```

#### Response

**Status:** 200 OK

```json
{
  "id_calificacion": 1,
  "id_estudiante": 1,
  "id_asignatura": 1,
  "periodo": "2025-1",
  "nota": 4.5,
  "observaciones": "Excelente rendimiento",
  "fecha_registro": "2025-06-09T10:00:00"
}
```

### Obtener una calificación por ID

**GET** `/calificaciones/{id_calificacion}`

#### Response

**Status:** 200 OK

```json
{
  "id_calificacion": 1,
  "id_estudiante": 1,
  "id_asignatura": 1,
  "periodo": "2025-1",
  "nota": 4.5,
  "observaciones": "Excelente rendimiento",
  "fecha_registro": "2025-06-09T10:00:00"
}
```

**Status:** 404 Not Found

```json
{
  "detail": "Calificacion not found"
}
```

### Listar todas las calificaciones

**GET** `/calificaciones/`

#### Response

**Status:** 200 OK

```json
[
  {
    "id_calificacion": 1,
    "id_estudiante": 1,
    "id_asignatura": 1,
    "periodo": "2025-1",
    "nota": 4.5,
    "observaciones": "Excelente rendimiento",
    "fecha_registro": "2025-06-09T10:00:00"
  },
  {
    "id_calificacion": 2,
    "id_estudiante": 2,
    "id_asignatura": 2,
    "periodo": "2025-1",
    "nota": 3.8,
    "observaciones": "Buen desempeño",
    "fecha_registro": "2025-06-09T10:30:00"
  }
]
```

## Instalación

1. Asegúrate de tener el entorno configurado:

   ```bash
   pip install -r requirements.txt
   ```
2. Configura la base de datos en el archivo `.env`:

   ```env
   DATABASE_URL="mysql+pymysql://user:password@host:port/database"
   ```
3. Ejecuta el servidor:

   ```bash
   uvicorn app.main:app --reload
   ```

## Pruebas

Para ejecutar las pruebas unitarias:

```bash
pytest app/tests/test_calificaciones.py
```

## Dependencias

* **FastAPI**: Framework principal.
* **SQLAlchemy**: ORM para manejar la base de datos.
* **Pytest**: Framework para pruebas unitarias.

## Contacto

Para más información, contactar con el equipo de desarrollo.
