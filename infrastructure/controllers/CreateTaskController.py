from application.services.create_task_service import CreateTaskService
from fastapi import APIRouter, Depends, status, HTTPException
from infrastructure.auth import oauth2
from pydantic import BaseModel, ValidationError


class CreateTaskRequestData(BaseModel):
    description: str
    difficult: int


router = APIRouter()
create_task_service = CreateTaskService()


@router.post("/api/v1/create_task", status_code=status.HTTP_200_OK)
async def create_task(request: CreateTaskRequestData, user_id: str = Depends(oauth2.require_user)):
    try:
        task_saved = create_task_service.create_task(owner_id=user_id, description=request.description, difficult=request.difficult)
        return task_saved
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The difficulty of the task should be between 1 and 10, with 1 being easy and 10 being difficult.")
