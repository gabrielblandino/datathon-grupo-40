"""Testes de endpoint FastAPI."""
from fastapi.testclient import TestClient
from generator.serving.app import app

client = TestClient(app)

def test_healthcheck():
    """Garante que a API está online."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "LLM Agent"}

def test_predict_endpoint_validation():
    """Garante que payload inválido seja barrado pelo FastAPI."""
    response = client.post("/api/v1/predict", json={"wrong_field": "data"})
    assert response.status_code == 422  # Unprocessable Entity (Erro de validação Pydantic)