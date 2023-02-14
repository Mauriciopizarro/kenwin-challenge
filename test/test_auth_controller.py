from fastapi.testclient import TestClient
from starter import app

client = TestClient(app)


def test_invalid_mail_auth_controller():
    response = client.post("/api/v1/login",
                           json={
                               "email": "nonexistent_email",
                               "password": "test123test",
                           },)

    assert response.status_code == 404
    assert response.json() == {"detail": "User does not exist"}


def test_invalid_password_auth_controller():
    response = client.post("/api/v1/login",
                           json={
                               "email": "mauripizarro14@gmail.com",
                               "password": "fake_password",
                           },)

    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect password"}


