from datetime import timedelta, datetime, timezone
from typing import Optional
from fastapi import HTTPException, APIRouter, Depends, Response, status, Request, Form
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from application.services.login_service import LoginService
from fastapi.responses import HTMLResponse
from config import settings
from infrastructure.auth.oauth2 import AuthJWT
from domain.models.User import IncorrectPasswordError
from infrastructure.exceptions.NotExistentUserException import NotExistentUserException

router = APIRouter()
template = Jinja2Templates(directory="./view")
login_service = LoginService()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN


class ResponseSchema(BaseModel):
    message: str
    access_token: str
    token_expires: Optional[datetime]


class LoginRequestData(BaseModel):
    email: str
    password: str


@router.get("/login", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def home_controller(req: Request):
    return template.TemplateResponse("login.html", {"request": req})


@router.post("/login", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def home_controller(req: Request):
    return template.TemplateResponse("login.html", {"request": req})


@router.post("/home", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def login(req: Request, response: Response, email: str = Form(), password_user: str = Form(), Authorize: AuthJWT = Depends()):
    try:
        user = login_service.login(email, password_user)

        # Create access token
        access_token = Authorize.create_access_token(
            subject=user.get_id(), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

        # Store access tokens in cookie
        response.set_cookie('access_token', access_token, max_age=ACCESS_TOKEN_EXPIRES_IN * 60,
                            expires=ACCESS_TOKEN_EXPIRES_IN * 60)

        response.set_cookie('logged_in', 'True', max_age=ACCESS_TOKEN_EXPIRES_IN * 60,
                            expires=ACCESS_TOKEN_EXPIRES_IN * 60)

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

    data = {"username": user.username, "email": user.email, "token": access_token}
    return template.TemplateResponse("home.html", {"request": req, "data_user": data})


@router.post('/api/v1/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)
    return {'detail': 'Session finished'}


@router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(req: Request, response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)
    return template.TemplateResponse("login.html", {"request": req})


@router.post("/api/v1/login", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
async def login(response: Response, request: LoginRequestData, Authorize: AuthJWT = Depends()):
    try:
        user = login_service.login(request.email, request.password)

        # Create access token
        access_token = Authorize.create_access_token(
            subject=user.get_id(), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

        # Store access tokens in cookie
        response.set_cookie('access_token', access_token, max_age=ACCESS_TOKEN_EXPIRES_IN * 60,
                            expires=ACCESS_TOKEN_EXPIRES_IN * 60)

        response.set_cookie('logged_in', 'True', max_age=ACCESS_TOKEN_EXPIRES_IN * 60,
                            expires=ACCESS_TOKEN_EXPIRES_IN * 60)

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
