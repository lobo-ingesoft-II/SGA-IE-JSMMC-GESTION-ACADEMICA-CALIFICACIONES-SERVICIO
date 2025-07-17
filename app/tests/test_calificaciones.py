from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

# Pruebas para endpoints de calificaciones

def test_create_calificacion_success():
    posibles_estudiantes = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]  # Asegúrate de que existan estos IDs en tu base de datos

    for estudiante_id in posibles_estudiantes:
        response = client.post("/", json={
            "id_estudiante": estudiante_id,
            "id_asignatura": 1,
            "periodo": "Primer Trimestre",
            "nota1": 4.5,
            "nota2": 3.8,
            "nota3": 4.2,
            "observaciones": "Buen desempeño"
        })

        if response.status_code in (200, 201):
            data = response.json()
            assert "nota1" in data
            assert "nota2" in data
            assert "nota3" in data
            print(f"✅ Calificación creada exitosamente para estudiante {estudiante_id}")
            break
        elif response.status_code == 400:
            detail = response.json().get("detail", "")
            if "ya existe" in detail.lower():
                continue  # probar siguiente estudiante
            else:
                assert False, f"Error 400 inesperado: {detail}"
        else:
            assert False, f"Error inesperado: {response.status_code} - {response.text}"
    else:
        assert False, "No se pudo crear una calificación para ningún estudiante disponible"


def test_create_calificacion_validation_error():
    # Falta campo obligatorio => 422 Unprocessable Entity
    response = client.post("/", json={
        "id_estudiante": 1,
        "periodo": "Primer Trimestre",
        "nota": 4.5
    })
    assert response.status_code == 422


def test_get_calificacion_success():
    response = client.get("/1")  # agregamos slash inicial
    assert response.status_code == 200
    assert response.json().get("id_calificacion") == 1


def test_get_calificacion_not_found():
    response = client.get("/999999")
    assert response.status_code == 404


def test_list_calificaciones():
    response = client.get("/")  # usamos ruta sin slash para evitar redirección
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_for_student_and_subject_success():
    response = client.post("/estudiante/3/asignatura/3", json={
        "periodo": "Tercer Trimestre",
        "nota1": 4.0,
        "nota2": 3.5,
        "nota3": 4.8,
        "observaciones": "Satisfactorio"
    })
    assert response.status_code in (200, 201)
    assert "nota1" in response.json()


def test_create_for_student_and_subject_validation_error():
    response = client.post("/estudiante/3/asignatura/3", json={
        "nota": 4.0
    })
    assert response.status_code == 422


def test_update_student_grades_success():

    update_resp = client.patch("/estudiante/1/asignatura/1", json={
        "periodo": "2025-1",
        "nota1": 4.5,
        "nota2": 4.0,
        "nota3": 4.0,
        "observaciones": "Test"
    })
    assert update_resp.status_code == 200
    assert update_resp.json().get("nota1") == 4.5


def test_update_student_grades_not_found():
    response = client.patch("/estudiante/9999/asignatura/9999", json={
        "nota": 4.2,
        "observaciones": "No existe"
    })
    assert response.status_code in (404, 422)


def test_get_by_student_and_subject_success():
    response = client.get("/estudiante/1/asignatura/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_by_student_and_subject_not_found():
    response = client.get("/estudiante/9999/asignatura/9999")
    assert response.status_code in (400,404, 422)


def test_list_by_estudiante_success():
    client.post("/calificacion", json={
        "id_estudiante": 6,
        "id_asignatura": 6,
        "periodo": "Sexto Trimestre",
        "nota1": 3.9,
        "nota2": 3.0,
        "nota3": 3.5,
        "observaciones": "Bien"
    })
    response = client.get("/por_estudiante/6")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_by_estudiante_not_found():
    response = client.get("/por_estudiante/9999")
    assert response.status_code in (400, 404, 422)


def test_list_by_asignatura_success():
    client.post("/", json={
        "id_estudiante": 7,
        "id_asignatura": 7,
        "periodo": "Séptimo Trimestre",
        "nota1": 4.1,
        "nota2": 4.0,
        "nota3": 4.2,
        "observaciones": "Bien"
    })
    response = client.get("/por_asignatura/7")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_by_asignatura_not_found():
    response = client.get("/por_asignatura/9999")
    assert response.status_code in (400, 404, 422)


def test_update_calificacion_success():
    update_resp = client.put(f"/2", json={
        "nota1": 3.5,
        "nota2": 3.5,
        "nota3": 3.5,
        "observaciones": "Mejoró un poco"
    })
    assert update_resp.status_code == 200
    data = update_resp.json()
    # Compruebo cada nota individualmente
    assert data["nota1"] == 3.5, f"Esperaba nota1=3.5, obtuve {data['nota1']}"
    assert data["nota2"] == 3.5, f"Esperaba nota2=3.5, obtuve {data['nota2']}"
    assert data["nota3"] == 3.5, f"Esperaba nota3=3.5, obtuve {data['nota3']}"
    # Y opcionalmente la observación
    assert data["observaciones"] == "Mejoró un poco"

def test_update_calificacion_not_found():
    response = client.put("/999999", json={
        "nota1": 3.0,
        "nota2": 3.0,
        "nota3": 3.0,
        "observaciones": "No existe"
    })
    assert response.status_code == 404


def test_partial_update_calificacion_success():
    patch_resp = client.patch(f"/1", json={
        "nota1": 1,
        "nota2": 1,
        "nota3": 1,
        "observaciones": "Test2"
    })
    assert patch_resp.status_code == 200
    data = patch_resp.json()
    # Compruebo cada nota individualmente
    assert data["nota1"] == 1, f"Esperaba nota1=1, obtuve {data['nota1']}"
    assert data["nota2"] == 1, f"Esperaba nota2=1, obtuve {data['nota2']}"
    assert data["nota3"] == 1, f"Esperaba nota3=1, obtuve {data['nota3']}"
    # Y opcionalmente la observación
    assert data["observaciones"] == "Test2"

def test_partial_update_calificacion_not_found():
    response = client.patch("/999999", json={
        "nota1": 4.8
    })
    assert response.status_code == 404


def test_custom_metrics():
    response = client.get("/custom_metrics")
    assert response.status_code == 200
