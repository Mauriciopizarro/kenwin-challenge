from fastapi.testclient import TestClient
from infrastructure.auth.oauth2 import require_user
from starter import app
from datetime import datetime, timedelta, timezone


async def mock_require_user():
    return "63e9c34684e9ed0fe6b498e4"


client = TestClient(app)
app.dependency_overrides[require_user] = mock_require_user
timezone_offset = -3.0  # Argentina Standard Time (UTC−03:00)
time_zone = timezone(timedelta(hours=timezone_offset))


def test_create_task():
    response = client.post("/api/v1/create_task",
                           json={
                               "description": "do something",
                               "difficult": 5
                           })
    assert response.status_code == 200
    assert response.json() == {
        "status": "in_progress",
        "owner_id": "63e9c34684e9ed0fe6b498e4",
        "description": "do something",
        "difficult": 5,
        "date_created": datetime.now(time_zone).strftime('%Y-%m-%dT%H:%M:%S'),
        "date_finished": None
    }


def test_difficult_out_of_range():
    response = client.post("/api/v1/create_task",
                           json={
                               "description": "do something",
                               "difficult": 12
                           })
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The difficulty of the task should be between 1 and 10, with 1 being easy and 10 being difficult."
    }
