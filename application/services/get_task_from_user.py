from domain.interfaces.TaskRepository import TaskRepository
from dependency_injector.wiring import Provide, inject
from infrastructure.Injector import Injector


class GetTaskFromUser:

    @inject
    def __init__(
            self, task_repository: TaskRepository = Provide[Injector.task_repo]
    ):
        self.task_repository = task_repository

    # filter method "all" to defect
    def get_task(self, owner_id, filter_by: str = 'all'):
        task_list = self.task_repository.get_all_by_owner_id(owner_id, filter_by)
        for task in task_list:
            del task['owner_id']
        return task_list
