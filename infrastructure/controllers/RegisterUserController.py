from pydantic import BaseModel
from application.services.register_user_service import RegisterUserService
from fastapi import HTTPException, APIRouter

router = APIRouter()
register_user_service = RegisterUserService()


class RegisterRequestData(BaseModel):
    email: str
    username: str
    password: str


class RegisterResponseData(BaseModel):
    #token: str
    username: str
    user_id: str
    email: str


@router.post("/api/v1/user/register", response_model=RegisterResponseData)
async def register_controller(request: RegisterRequestData):
    return register_user_service.register_user(request.email, request.username, request.password)
