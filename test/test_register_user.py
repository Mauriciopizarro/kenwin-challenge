from application.services.register_user_service import RegisterUserService
from infrastructure.exceptions.InvalidMinCharactersPasswordException import InvalidMinCharactersPasswordException
from test.utils.mock_user_repositotory import MockUserRepository
import pytest
import pymongo
import mongomock


#arrange
mock_user_repository = MockUserRepository()
register_user_service = RegisterUserService(user_repository=mock_user_repository)


@mongomock.patch(
    servers=(("mongodb://null:null@localhost/test", 27017),), on_new="pymongo"
)
def get_mongodb_table():
    return pymongo.MongoClient('mongodb://null:null@localhost/test')['test']['table']


def test_mongo_insert():
    table = get_mongodb_table()
    table.insert_one({'username': 'mpizarro', "email": "test@gmail.com"})
    user = table.find_one({})

    assert user.get("username") == "mpizarro"
    assert user.get("email") == "test@gmail.com"
    assert user.get("_id").__class__.__name__ == "ObjectId"


#act
def test_register_user():
    #Happy path
    user_dict = register_user_service.register_user("test@gmail.com", "mpizarro", "Manzana123..")

    # assert
    assert user_dict.get("username") == "mpizarro"
    assert user_dict.get("email") == "test@gmail.com"


def test_short_pass():
    # If players is empty raise exception EmptyPlayersList
    with pytest.raises(InvalidMinCharactersPasswordException):
        register_user_service.register_user("test@gmail.com", "mpizarro", "12345") # password short, less 8 characters


def test_long_pass():
    # If players is empty raise exception EmptyPlayersList
    with pytest.raises(InvalidMinCharactersPasswordException):
        register_user_service.register_user("test@gmail.com", "mpizarro", "123456789123456789") # password long, more to 14 characters
