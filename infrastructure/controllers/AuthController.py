from datetime import timedelta, datetime, timezone
from typing import Optional
from fastapi import HTTPException, APIRouter, Depends, Response, status
from pydantic import BaseModel
from application.services.login_service import LoginService
from config import settings
from infrastructure.auth.oauth2 import AuthJWT
from domain.models.User import IncorrectPasswordError
from infrastructure.exceptions.NotExistentUserException import NotExistentUserException

router = APIRouter()
login_service = LoginService()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN


class ResponseSchema(BaseModel):
    message: str
    access_token: str
    token_expires: Optional[datetime]


class LoginRequestData(BaseModel):
    email: str
    password: str


@router.post("/api/v1/login", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
async def login(request: LoginRequestData, response: Response, Authorize: AuthJWT = Depends()):
    try:
        user = login_service.login(request.email, request.password)

        # Create access token
        access_token = Authorize.create_access_token(
            subject=user.get_id(), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

        # Store access tokens in cookie
        response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                            ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
        response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                            ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

        timezone_offset = -3.0  # Argentina Standard Time (UTC−03:00)
        tzinfo = timezone(timedelta(hours=timezone_offset))
        token_expire_date = datetime.now(tzinfo) + timedelta(minutes=(ACCESS_TOKEN_EXPIRES_IN * 60))

    except NotExistentUserException:
        raise HTTPException(
            status_code=404,
            detail="User does not exist",
        )
    except IncorrectPasswordError:
        raise HTTPException(
            status_code=400,
            detail="Incorrect password",
        )

    return {"message": "Success",
            "access_token": access_token,
            "token_expires": token_expire_date}


@router.post('/api/v1/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)
    return {'status': 'Session finished'}
