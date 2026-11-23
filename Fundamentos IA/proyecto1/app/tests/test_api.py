from fastapi.testclient import TestClient
from app.main import app
#from app.schemas import SolicitudIn, ClassificacionOut

client = TestClient(app)

def test_health()-> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_incidente_urgente()-> None:
    response = client.post("/classificar", json={"cliente": "Juan Perez", "mensaje": "Mi internet no funciona", "canal": "web"})
    assert response.status_code == 200
    assert response.json()["prioridad"] == "alta"
    assert response.json()["requiere_atencion"] == True

def test_rechaza_mensaje_corto()-> None:
    response = client.post("/classificar", json={"cliente": "Juan Perez", "mensaje": "hola", "canal": "web"})
    assert response.status_code == 422
    # assert response.json()["detail"][0]["loc"] == ["body", "mensaje"]
    # assert response.json()["detail"][0]["msg"] == "ensure this value has at least 5 characters"