import uuid
from fastapi.testclient import TestClient
from fastapi import status
from testforpatres.main import app  # замени путь при необходимости

client = TestClient(app)


def test_access_control_for_endpoints():
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

    public_response = client.get("/books/")
    assert public_response.status_code == status.HTTP_200_OK

    unauthorized_response = client.get("/readers/")
    assert unauthorized_response.status_code == status.HTTP_403_FORBIDDEN

    authorized_response = client.get("/readers/", headers=headers)
    assert authorized_response.status_code == status.HTTP_200_OK
