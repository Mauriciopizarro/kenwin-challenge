import logging
from dependency_injector.wiring import Provide, inject
from domain.interfaces.TaskRepository import TaskRepository
from infrastructure.Injector import Injector
from datetime import datetime, timedelta, timezone

from infrastructure.exceptions.TaskAlreadyFinishedException import TaskAlreadyFinishedException


class FinishTaskService:

    @inject
    def __init__(
            self, task_repository: TaskRepository = Provide[Injector.task_repo]
    ):
        self.task_repository = task_repository

    def finish_task(self, task_id):
        task = self.task_repository.get_by_id(task_id)
        if task.status == "finished":
            raise TaskAlreadyFinishedException()
        task.finish_task()
        timezone_offset = -3.0  # Argentina time zone (UTC−03:00)
        time_zone = timezone(timedelta(hours=timezone_offset))
        task.date_finished = datetime.now(time_zone).strftime('%Y-%m-%dT%H:%M:%S')
        self.task_repository.update(task_id, task)
        return task
