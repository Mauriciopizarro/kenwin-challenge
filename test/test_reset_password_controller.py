from fastapi.testclient import TestClient
from infrastructure.auth.oauth2 import require_user
from starter import app


async def mock_require_user():
    return "63e9c34684e9ed0fe6b498e4"


client = TestClient(app)
app.dependency_overrides[require_user] = mock_require_user


def test_empty_new_password():
    response = client.post("/api/v1/reset_password",
                           json={
                               "new_password": "",
                               "repeat_new_password": "asd123asd123",
                           },)

    assert response.status_code == 400
    assert response.json() == {"detail": "new_password field is empty"}


def test_not_match_passwords():
    response = client.post("/api/v1/reset_password",
                           json={
                               "new_password": "test123test",
                               "repeat_new_password": "not_match",
                           },)

    assert response.status_code == 400
    assert response.json() == {"detail": "Password are not matching, try again"}
