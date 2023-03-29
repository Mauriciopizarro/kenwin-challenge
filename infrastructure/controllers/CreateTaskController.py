from application.services.create_task_service import CreateTaskService
from fastapi import APIRouter, Depends, status, HTTPException, Form, Request
from application.services.get_task_service import GetTaskFromUser
from infrastructure.auth import oauth2
from pydantic import BaseModel, ValidationError
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from infrastructure.exceptions.IncorrectObjectIdException import IncorrectObjectIdException
from infrastructure.exceptions.TaskNotFoundException import TaskNotFoundException


class CreateTaskRequestData(BaseModel):
    description: str
    difficult: int


router = APIRouter()
create_task_service = CreateTaskService()
get_task_from_user = GetTaskFromUser()
template = Jinja2Templates(directory="./view")


@router.get("/create_new_task", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def create_task(req: Request):
    return template.TemplateResponse("create_task.html", {"request": req})


# get task for task_id, after task is created, this method is called
@router.post("/get_task/{task_id}", status_code=status.HTTP_200_OK)
async def get_task(req: Request, task_id: str, user_id: str = Depends(oauth2.require_user)):
    try:
        task_json = get_task_from_user.get_by_id_in_json_format(task_id)
        return template.TemplateResponse("task_details.html", {"request": req, "data_task": task_json})
    except TaskNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    except IncorrectObjectIdException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect task_id format")


@router.post("/create_task", status_code=status.HTTP_200_OK)
async def create_task(difficult: str = Form(), description: str = Form(), user_id: str = Depends(oauth2.require_user)):
    try:
        task_saved = create_task_service.create_task(owner_id=user_id, description=description, difficult=difficult)

        url_to_response = "/get_task/" + str(task_saved.id)
        return RedirectResponse(url_to_response)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The difficulty of the task should be between 1 and 10, with 1 being easy and 10 being difficult.")


@router.post("/api/v1/create_task", status_code=status.HTTP_200_OK)
async def create_task(request: CreateTaskRequestData, user_id: str = Depends(oauth2.require_user)):
    try:
        task_saved = create_task_service.create_task(owner_id=user_id, description=request.description, difficult=request.difficult)
        return task_saved
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The difficulty of the task should be between 1 and 10, with 1 being easy and 10 being difficult.")
