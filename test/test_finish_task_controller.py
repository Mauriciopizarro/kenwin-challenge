from unittest.mock import patch
from fastapi.testclient import TestClient
from application.services.finish_task_service import FinishTaskService
from infrastructure.auth.oauth2 import require_user
from starter import app
from datetime import datetime, timedelta, timezone


async def mock_require_user():
    return "63e9c34684e9ed0fe6b498e4"


client = TestClient(app)
app.dependency_overrides[require_user] = mock_require_user
timezone_offset = -3.0  # Argentina Standard Time (UTC−03:00)
time_zone = timezone(timedelta(hours=timezone_offset))


@patch.object(FinishTaskService, 'finish_task')
def test_finish_task(mock_finish_task):
    response = client.post("/api/v1/finish_task/63e9d4aaf3fdfd95f9bdf463")
    assert response.status_code == 200
    mock_finish_task.assert_called_once_with("63e9d4aaf3fdfd95f9bdf463")


def test_cant_finish_task():
    response = client.post("/api/v1/finish_task/63e932b0069ebc836b2734f8")
    assert response.json() == {
        "detail": "Task is already finished"
    }


def test_task_incorrect_format():
    response = client.post("/api/v1/finish_task/bad_format_task_id")
    assert response.json() == {
        "detail": "Incorrect task_id format"
    }

