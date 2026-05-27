from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_aeroporti_pagination():
    response = client.get("/aeroporti?page=1&size=2")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2

def test_create_aeroporto_unauthorized():
    response = client.post("/aeroporti", json={"codice": "LIN", "citta": "Milano"})
    assert response.status_code == 422 # Manca l'header Authorization

def test_create_aeroporto_authorized():
    headers = {"Authorization": "Bearer mio-token-segreto"}
    response = client.post("/aeroporti", json={"codice": "LIN", "citta": "Milano"}, headers=headers)
    assert response.status_code == 201
    assert response.json()["codice"] == "LIN"