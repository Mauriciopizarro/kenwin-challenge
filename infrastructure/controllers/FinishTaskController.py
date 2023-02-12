from fastapi import APIRouter, status, HTTPException
from application.services.finish_task_service import FinishTaskService
from infrastructure.exceptions.IncorrectObjectIdException import IncorrectObjectIdException
from infrastructure.exceptions.TaskAlreadyFinishedException import TaskAlreadyFinishedException
from infrastructure.exceptions.TaskNotFoundException import TaskNotFoundException

router = APIRouter()
finish_task_service = FinishTaskService()


@router.post("/api/v1/finish_task/{task_id}", status_code=status.HTTP_200_OK)
async def finish_task(task_id: str):
    try:
        task = finish_task_service.finish_task(task_id)
        return task
    except TaskNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    except TaskAlreadyFinishedException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Task is already finished")
    except IncorrectObjectIdException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect task_id format")
