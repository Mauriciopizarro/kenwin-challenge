from pydantic import BaseModel, ValidationError
from application.services.register_user_service import RegisterUserService
from fastapi import HTTPException, APIRouter
from infrastructure.exceptions.EmailUsedException import EmailUsedException
from infrastructure.exceptions.InvalidMinCharactersPasswordException import InvalidMinCharactersPasswordException
from infrastructure.exceptions.NotExistentUserException import NotExistentUserException
from infrastructure.exceptions.UserExistentException import UserExistentException
from infrastructure.exceptions.UsernameUsedException import UsernameUsedException

router = APIRouter()
register_user_service = RegisterUserService()


class RegisterRequestData(BaseModel):
    email: str
    username: str
    password: str


class RegisterResponseData(BaseModel):
    username: str
    user_id: str
    email: str


@router.post("/api/v1/register", status_code=201, response_model=RegisterResponseData)
async def register_controller(request: RegisterRequestData):
    try:
        return register_user_service.register_user(request.email, request.username, request.password)
    except UserExistentException:
        raise HTTPException(status_code=400,
                            detail="Username already in use")
    except InvalidMinCharactersPasswordException:
        raise HTTPException(status_code=400,
                            detail="Password should have between 8 and 14 characters")
    except ValidationError:
        raise HTTPException(status_code=400,
                            detail="Email not valid")
    except EmailUsedException:
        raise HTTPException(status_code=400,
                            detail="Email in use, try other or reset your password")
    except NotExistentUserException:
        raise HTTPException(status_code=404,
                            detail="User not found")
    except UsernameUsedException:
        raise HTTPException(status_code=404,
                            detail="Username in use")
