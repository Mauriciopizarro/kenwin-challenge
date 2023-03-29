from domain.interfaces.TaskRepository import TaskRepository
from dependency_injector.wiring import Provide, inject
from domain.models.Task import Task
from datetime import datetime, timedelta, timezone
from infrastructure.Injector import Injector


class CreateTaskService:

    @inject
    def __init__(
            self, task_repository: TaskRepository = Provide[Injector.task_repo]
    ):
        self.task_repository = task_repository

    def create_task(self, owner_id, description,  difficult):
        timezone_offset = -3.0  # Argentina Standard Time (UTC−03:00)
        time_zone = timezone(timedelta(hours=timezone_offset))
        task = Task(status="in_progress", owner_id=owner_id, description=description, difficult=difficult, date_created=datetime.now(time_zone).strftime('%Y-%m-%d %H:%M:%S'), date_finished=None)
        task_created = self.task_repository.save(task)
        task.id = task_created.inserted_id
        return task
