from pydantic import BaseModel, ValidationError
from application.services.register_user_service import RegisterUserService
from fastapi import HTTPException, APIRouter, status, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from infrastructure.exceptions.EmailUsedException import EmailUsedException
from infrastructure.exceptions.InvalidMinCharactersPasswordException import InvalidMinCharactersPasswordException
from infrastructure.exceptions.NotExistentUserException import NotExistentUserException
from infrastructure.exceptions.UserExistentException import UserExistentException
from infrastructure.exceptions.UsernameUsedException import UsernameUsedException

router = APIRouter()
template = Jinja2Templates(directory="./view")
register_user_service = RegisterUserService()


class RegisterRequestData(BaseModel):
    email: str
    username: str
    password: str


class RegisterResponseData(BaseModel):
    username: str
    user_id: str
    email: str


@router.get("/register", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def register_controller(req: Request):
    return template.TemplateResponse("register.html", {"request": req})


@router.post("/api/v1/register", status_code=status.HTTP_201_CREATED, response_model=RegisterResponseData)
async def register_controller(request: RegisterRequestData):
    try:
        return register_user_service.register_user(request.email, request.username, request.password)
    except UserExistentException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username already in use")
    except InvalidMinCharactersPasswordException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password should have between 8 and 14 characters")
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email not valid")
    except EmailUsedException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email in use, try other or reset your password")
    except NotExistentUserException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    except UsernameUsedException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username in use")


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=RegisterResponseData)
def register(username: str = Form(), email: str = Form(), password_user: str = Form()):
    try:
        register_user_service.register_user(email, username, password_user)
        return RedirectResponse("/login")
    except UserExistentException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username already in use")
    except InvalidMinCharactersPasswordException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Password should have between 8 and 14 characters")
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email not valid")
    except EmailUsedException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email in use, try other or reset your password")
    except NotExistentUserException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    except UsernameUsedException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username in use")
