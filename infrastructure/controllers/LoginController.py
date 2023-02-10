from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from application.services.login_service import LoginService
from domain.models.User import IncorrectPasswordError
from infrastructure.exceptions.NotExistentUserException import NotExistentUserException

router = APIRouter()
login_service = LoginService()


class ResponseSchema(BaseModel):
    message: str
    #access_token: str
    #token_type: str


class LoginRequestData(BaseModel):
    email: str
    password: str


@router.post("/api/v1/login", response_model=ResponseSchema)
async def login(request: LoginRequestData):
    try:
        user = login_service.login(request.email, request.password)
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
    #access_token = TokenService.generate_token(user)
    return {"message": "Correct credentials, welcome " + user.get_username()}
