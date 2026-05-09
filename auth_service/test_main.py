import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def test_app():
    yield app

def test_successful_login(test_app):
    response = client.post("/login", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]

def test_invalid_login(test_app):
    response = client.post("/login", json={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Bad credentials"