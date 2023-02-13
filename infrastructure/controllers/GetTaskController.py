from application.services.get_task_from_user import GetTaskFromUser
from fastapi import APIRouter, Depends, status
from infrastructure.auth import oauth2


router = APIRouter()
get_task_service = GetTaskFromUser()


@router.get("/api/v1/tasks", status_code=status.HTTP_200_OK)
async def get_tasks(user_id: str = Depends(oauth2.require_user)):
    tasks = get_task_service.get_task(user_id)
    return tasks
