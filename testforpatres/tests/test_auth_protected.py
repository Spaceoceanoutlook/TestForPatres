from fastapi.testclient import TestClient
from testforpatres.main import app
from fastapi import status
import uuid

client = TestClient(app)

def test_protected_endpoint_access():
    unique_email = f"user_{uuid.uuid4()}@example.com"
    response = client.post("/auth/register", json={
        "email": unique_email,
        "password": "string"
    })
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post("/auth/login", json={
        "email": unique_email,
        "password": "string"
    })
    assert response.status_code == status.HTTP_200_OK

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    protected_response = client.get("/books/", headers=headers)
    assert protected_response.status_code == status.HTTP_200_OK

    unprotected_response = client.get("/readers/")
    assert unprotected_response.status_code == status.HTTP_403_FORBIDDEN

