from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_calificacion():
    response = client.post("/calificaciones/", json={
        "id_estudiante": 1,
        "id_asignatura": 1,
        "periodo": "Primer Trimestre",
        "nota": 4.5,
        "observaciones": "Buen desempeño"
    })
    assert response.status_code == 200
    assert response.json()["nota"] == 4.5

def test_get_calificacion():
    response = client.get("/calificaciones/1")
    assert response.status_code == 200
    assert "id_estudiante" in response.json()

def test_list_calificaciones():
    response = client.get("/calificaciones/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)