from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_aeroporti():
    response = client.get("/aeroporti")
    assert response.status_code == 200
    json_data = response.json()
    assert "page" in json_data
    assert "size" in json_data
    assert "total" in json_data
    assert "data" in json_data

def test_get_aeroporto_valido():
    response = client.get("/aeroporti/1")
    assert response.status_code == 200
    assert response.json()["codice"] == "MXP"

def test_get_aeroporto_non_trovato():
    response = client.get("/aeroporti/999")
    assert response.status_code == 404

def test_create_aeroporto_senza_token():
    payload = {"codice": "LIN", "citta": "Milano"}
    response = client.post("/aeroporti", json=payload)
    assert response.status_code == 422 or response.status_code == 401

def test_create_aeroporto_con_token():
    headers = {"Authorization": "Bearer mio-token-segreto"}
    payload = {"codice": "LIN", "citta": "Milano"}
    response = client.post("/aeroporti", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["codice"] == "LIN"

def test_create_aeroporto_validazione_errata():
    headers = {"Authorization": "Bearer mio-token-segreto"}
    payload = {"codice": "TROPPO_LUNGO", "citta": "Milano"}
    response = client.post("/aeroporti", json=payload, headers=headers)
    assert response.status_code == 422

def test_delete_aeroporto_non_trovato():
    headers = {"Authorization": "Bearer mio-token-segreto"}
    response = client.delete("/aeroporti/999", headers=headers)
    assert response.status_code == 404
