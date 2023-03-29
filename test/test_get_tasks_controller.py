from unittest.mock import patch
from fastapi.testclient import TestClient
from application.services.get_task_service import GetTaskFromUser
from infrastructure.auth.oauth2 import require_user
from starter import app


async def mock_require_user():
    return "63e9c34684e9ed0fe6b498e4"


client = TestClient(app)
app.dependency_overrides[require_user] = mock_require_user


@patch.object(GetTaskFromUser, 'get_task')
def test_finish_task(mock_get_task):
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    mock_get_task.assert_called_once_with("63e9c34684e9ed0fe6b498e4")
