# Servicio de Calificaciones

## Descripción

Este servicio gestiona las calificaciones de los estudiantes en el sistema académico. Permite crear, obtener y listar calificaciones, así como consultar calificaciones por estudiante o por asignatura. Antes de registrar o consultar calificaciones por estudiante o asignatura, el servicio valida la existencia de estos recursos en los servicios externos correspondientes.

---

## Endpoints

### Crear una calificación

**POST** `/calificaciones/`

Valida que el `id_estudiante` y el `id_asignatura` existan en los servicios externos antes de registrar la calificación.

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

**Status:** 400 Bad Request

```json
{
  "detail": "El estudiante no existe"
}
```
o
```json
{
  "detail": "La asignatura no existe"
}
```

---

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

---

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
  }
]
```

---

### Listar calificaciones por estudiante

**GET** `/calificaciones/por_estudiante/{id_estudiante}`

Valida que el estudiante exista en el servicio externo antes de devolver las calificaciones.

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
  }
]
```

**Status:** 400 Bad Request

```json
{
  "detail": "El estudiante no existe"
}
```

---

### Listar calificaciones por asignatura

**GET** `/calificaciones/por_asignatura/{id_asignatura}`

Valida que la asignatura exista en el servicio externo antes de devolver las calificaciones.

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
  }
]
```

**Status:** 400 Bad Request

```json
{
  "detail": "La asignatura no existe"
}
```

---

## Validaciones externas

- **id_estudiante**: Se valida contra el servicio externo de estudiantes antes de registrar o consultar calificaciones.
- **id_asignatura**: Se valida contra el servicio externo de asignaturas antes de registrar o consultar calificaciones.

---

## Instalación

1. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Configura la base de datos en el archivo `.env`:

   ```env
   DATABASE_URL="mysql+pymysql://user:password@host:port/calificaciones_db"
   ```

3. Ejecuta el servidor:

   ```bash
   uvicorn app.main:app --reload --port 8003
   ```

---

## Pruebas

Para ejecutar las pruebas unitarias:

```bash
pytest app/test/test_calificaciones.py
```

---

## Documentación interactiva

Accede a la documentación Swagger en [http://localhost:8003/docs](http://localhost:8003/docs)  
o ReDoc en [http://localhost:8003/redoc](http://localhost:8003/redoc).

---

## Contacto

Para más información, contactar con el equipo de desarrollo.