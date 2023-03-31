from application.services.get_task_service import GetTaskFromUser
from fastapi import APIRouter, Depends, status, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from infrastructure.auth import oauth2
import json

from infrastructure.exceptions.IncorrectObjectIdException import IncorrectObjectIdException
from infrastructure.exceptions.NotSameOwnerTaskException import NotSameOwnerTaskException

router = APIRouter()
get_task_service = GetTaskFromUser()
template = Jinja2Templates(directory="./view")


@router.get("/my_tasks/{filter_by}", status_code=status.HTTP_200_OK)
async def get_tasks(filter_by: str, req: Request, user_id: str = Depends(oauth2.require_user)):
    tasks = get_task_service.get_by_owner(user_id, filter_by)
    json_response = json.dumps(tasks)
    return template.TemplateResponse("my_tasks.html", {"request": req, "data_task": json_response})


@router.get("/api/v1/tasks/{filter_by}", status_code=status.HTTP_200_OK)
async def get_tasks(filter_by: str, user_id: str = Depends(oauth2.require_user)):
    tasks = get_task_service.get_by_owner(user_id, filter_by)
    return tasks


@router.post("/get_task", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_by_id(req: Request, task_id: str = Form(), owner_id: str = Depends(oauth2.require_user)):
    try:
        task = get_task_service.get_by_id_in_json_format(task_id, owner_id)
    except IncorrectObjectIdException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect task_id provided")
    except NotSameOwnerTaskException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You are not the owner of the task provider")
    return template.TemplateResponse("task_details.html", {"request": req, "data_task": task})


@router.get("/search_task_by_id", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def home_controller(req: Request):
    return template.TemplateResponse("search_task.html", {"request": req})
