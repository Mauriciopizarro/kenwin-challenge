from pymongo import MongoClient
from bson.objectid import ObjectId
from domain.interfaces.UserRepository import UserRepository
from domain.models.User import UserDatabaseModel, UserPlainPassword
from infrastructure.Exceptions.NotExistentUserException import NotExistentUserException
from infrastructure.Exceptions.UserExistentException import UserExistentException


class MongoUserRepository(UserRepository):

    instance = None

    def __init__(self):
        self.db = self.get_database()

    #Singleton pattern
    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()

        return cls.instance

    @staticmethod
    def get_database():
        client = MongoClient("mongodb://mongo:27017/kenwin")
        return client['kwnwin']["users"]

    def get_by_username(self, username):
        user_dict = self.db.find_one({"username": username})
        if user_dict is None:
            raise NotExistentUserException()
        user_dict.update({'_id': str(user_dict.get('_id'))})
        user_dict["id"] = user_dict.pop('_id')
        return UserDatabaseModel(**user_dict)

    def save_user(self, user: UserPlainPassword):
        user_dict = self.db.find_one({"username": user.get_username()})
        if user_dict:
            raise UserExistentException()
        hashed_password = user.get_hashed_password()
        user_id = self.db.insert_one({"username": user.get_username(), "email": user.get_email(), "hashed_password": hashed_password})
        return UserDatabaseModel(hashed_password=hashed_password, id=str(user_id.inserted_id), username=user.get_username(), email=user.get_email())

    def update_password(self, user: UserDatabaseModel):
        user_dict = user.dict()
        user_dict.pop("id")
        self.db.find_one_and_update({"_id": ObjectId(user.get_id())}, {"$set": user_dict})
