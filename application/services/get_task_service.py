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
    def get_by_owner(self, owner_id, filter_by: str = 'all'):
        task_list = self.task_repository.get_all_by_owner_id(owner_id, filter_by)
        for task in task_list:
            del task['owner_id']
        return task_list

    def get_by_id_in_json_format(self, task_id):
        task = self.task_repository.get_by_id(task_id)
        task_json = {
            "status": task.status,
            "id": task.id,
            "description": task.description,
            "difficult": task.difficult,
            "date_created": task.date_created,
            "date_finished": task.date_finished
        }
        return task_json
