from fastapi.testclient import TestClient
from starter import app

client = TestClient(app)


def test_register_invalid_password_characters():
    response = client.post("/api/v1/register",
                           json={
                               "username": "test",
                               "email": "test@test.com",
                               "password": "123.",
                           },)

    assert response.status_code == 400
    assert response.json() == {"detail": "Password should have between 8 and 14 characters"}


def test_register_invalid_email():
    response = client.post("/api/v1/register",
                           json={
                               "username": "test",
                               "email": "bad_email",
                               "password": "123456789",
                           },)

    assert response.status_code == 400
    assert response.json() == {"detail": "Email not valid"}

