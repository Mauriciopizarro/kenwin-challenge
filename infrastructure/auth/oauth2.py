import base64
import logging
from typing import List
from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from config import settings
from infrastructure.repositories.mongo_user_repository import MongoUserRepository


class Settings(BaseModel):
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(
        settings.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        settings.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return Settings()


class UserNotFound(Exception):
    pass


def require_user(Authorize: AuthJWT = Depends()):
    mongodb = MongoUserRepository()

    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        user = mongodb.get_database().find_one({'_id': ObjectId(str(user_id))})

        if not user:
            raise UserNotFound('User no longer exist')

    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=401,
                detail='You are not logged in')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=404,
                detail='User no longer exist')
        raise HTTPException(
            status_code=401,
            detail='Token is invalid or has expired')
    return user_id
