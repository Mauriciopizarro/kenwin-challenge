from bson import ObjectId
from bson.json_util import dumps
import json
from domain.interfaces.TaskRepository import TaskRepository
from pymongo import MongoClient
from config import settings
from domain.models.Task import Task
from infrastructure.exceptions.IncorrectObjectIdException import IncorrectObjectIdException
from infrastructure.exceptions.NotSameOwnerTaskException import NotSameOwnerTaskException
from infrastructure.exceptions.TaskNotFoundException import TaskNotFoundException


class MongoTaskRepository(TaskRepository):

    def __init__(self):
        self.db = self.get_database()

    @staticmethod
    def get_database():
        client = MongoClient(settings.DATABASE_URL).get_database("kenwin").get_collection("task")
        return client

    def get_all_by_owner_id(self, owner_id: str, filter_by: str):

        if filter_by == "all":
            task_list = self.db.find({"owner_id": owner_id})
            json_data = dumps(task_list)
            json_response = json.loads(json_data)
            formated_response = self.format_model_response(json_response)
            return formated_response

        task_list = self.db.find({"status": filter_by, "owner_id": owner_id})
        json_data = dumps(task_list)
        json_response = json.loads(json_data)
        formated_response = self.format_model_response(json_response)
        return formated_response

    def get_by_id(self, task_id: str, owner_id) -> Task:
        if not ObjectId.is_valid(task_id):
            raise IncorrectObjectIdException()
        task_dict = self.db.find_one({"_id": ObjectId(task_id)})
        if not task_dict:
            raise TaskNotFoundException()
        if task_dict.get("owner_id") != owner_id:
            raise NotSameOwnerTaskException()
        if task_dict.get("status") == "finished":
            return Task(status=task_dict["status"],
                        id=str(task_dict["_id"]),
                        owner_id=task_dict["owner_id"],
                        description=task_dict["description"],
                        difficult=task_dict["difficult"],
                        date_created=(task_dict["date_created"]),
                        date_finished=(task_dict["date_finished"]))

        return Task(status=task_dict["status"],
                    id=str(task_dict["_id"]),
                    owner_id=task_dict["owner_id"],
                    description=task_dict["description"],
                    difficult=task_dict["difficult"],
                    date_created=(task_dict["date_created"])
                    )

    def save(self, task: Task):
        return self.db.insert_one(task.dict())

    def update(self, task_id, task):
        if not ObjectId.is_valid(task_id):
            raise IncorrectObjectIdException()
        self.db.find_one_and_update({"_id": ObjectId(task_id)}, {"$set": task.dict()}, {'_id': 0})

    @staticmethod
    def format_model_response(json_response: dict) -> dict:
        for results in json_response:
            task_id = results.get("_id").get("$oid")
            results["id"] = task_id
            results.pop("_id")
            date_created = str(results.get("date_created").get("$date"))
            results.pop("date_created")
            results["date_created"] = date_created
        return json_response

