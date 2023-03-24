from application.services.get_task_from_user import GetTaskFromUser
from fastapi import APIRouter, Depends, status, Request
from fastapi.templating import Jinja2Templates
from infrastructure.auth import oauth2


router = APIRouter()
get_task_service = GetTaskFromUser()
template = Jinja2Templates(directory="./view")


@router.get("/my_tasks", status_code=status.HTTP_200_OK)
async def get_tasks(req: Request, user_id: str = Depends(oauth2.require_user)):
    tasks = get_task_service.get_task(user_id)
    return template.TemplateResponse("my_tasks.html", {"request": req, "data_task": tasks})


@router.get("/api/v1/tasks", status_code=status.HTTP_200_OK)
async def get_tasks(user_id: str = Depends(oauth2.require_user)):
    tasks = get_task_service.get_task(user_id)
    return tasks
