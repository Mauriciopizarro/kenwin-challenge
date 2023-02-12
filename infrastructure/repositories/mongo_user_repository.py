from pymongo import MongoClient
from bson.objectid import ObjectId
from config import settings
from domain.interfaces.UserRepository import UserRepository
from domain.models.User import UserDatabaseModel, UserPlainPassword
from infrastructure.exceptions.EmailUsedException import EmailUsedException
from infrastructure.exceptions.NotExistentUserException import NotExistentUserException
from infrastructure.exceptions.UsernameUsedException import UsernameUsedException


class MongoUserRepository(UserRepository):

    def __init__(self):
        self.db = self.get_database()

    @staticmethod
    def get_database():
        client = MongoClient(settings.DATABASE_URL).get_database("kenwin").get_collection("users")
        return client

    def get_by_username(self, username, is_user_register=False):
        user_dict = self.db.find_one({"username": username})

        if is_user_register and user_dict:
            raise UsernameUsedException()

        if user_dict is None:
            if not is_user_register:
                raise NotExistentUserException()

        if is_user_register and user_dict is None:
            return None

        user_dict.update({'_id': str(user_dict.get('_id'))})
        user_dict["id"] = user_dict.pop('_id')
        return UserDatabaseModel(**user_dict)

    def get_by_email(self, email, is_user_register=False):
        user_dict = self.db.find_one({"email": email})

        if is_user_register and user_dict:
            raise EmailUsedException()

        if user_dict is None:
            if not is_user_register:
                raise NotExistentUserException()

        if is_user_register and user_dict is None:
            return None

        user_dict.update({'_id': str(user_dict.get('_id'))})
        user_dict["id"] = user_dict.pop('_id')
        return UserDatabaseModel(**user_dict)

    def save_user(self, user: UserPlainPassword):
        hashed_password = user.get_hashed_password()
        user_id = self.db.insert_one({"username": user.get_username(), "email": user.get_email(), "hashed_password": hashed_password})
        return UserDatabaseModel(hashed_password=hashed_password, id=str(user_id.inserted_id), username=user.get_username(), email=user.get_email())

    def update_password(self, user: UserDatabaseModel):
        user_dict = user.dict()
        user_dict.pop("id")
        self.db.find_one_and_update({"_id": ObjectId(user.get_id())}, {"$set": user_dict})
