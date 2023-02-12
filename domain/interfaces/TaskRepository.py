from abc import ABC, abstractmethod
from domain.models.Task import Task


class TaskRepository(ABC):

    @abstractmethod
    def get_all_by_owner_id(self, owner_id: str):
        pass

    @abstractmethod
    def get_by_id(self, task_id: str) -> Task:
        pass

    @abstractmethod
    def save(self, task: Task):
        pass

    @abstractmethod
    def update(self, task_id, task):
        pass
