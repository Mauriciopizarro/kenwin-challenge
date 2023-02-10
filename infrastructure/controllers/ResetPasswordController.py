from bson import ObjectId
from application.services.reset_password_service import ResetPasswordService, EmptyNewPassword
from pydantic import BaseModel
from fastapi import HTTPException, APIRouter, Depends
from infrastructure.auth import oauth2
from infrastructure.repositories.mongo_user_repository import MongoUserRepository

router = APIRouter()
reset_password_service = ResetPasswordService()


class ResetPasswordRequestData(BaseModel):
    new_password: str
    repeat_new_password: str


class NotExistentUser(Exception):
    pass


@router.post("/api/v1/reset_password", status_code=200)
async def reset_password_controller(request: ResetPasswordRequestData, user_id: str = Depends(oauth2.require_user)):
    try:
        mongodb = MongoUserRepository()
        user = mongodb.get_database().find_one({'_id': ObjectId(str(user_id))})
        if request.new_password == request.repeat_new_password:
            reset_password_service.reset_password(user_name=user.get("username"), new_password=request.new_password)
        else:
            raise HTTPException(
                status_code=400,
                detail="Password are not matching, try again",
            )
    except NotExistentUser:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    except EmptyNewPassword:
        raise HTTPException(
            status_code=400,
            detail="'new_password' field is empty",
        )
    return {"message": "Password has been updated successfully"}
