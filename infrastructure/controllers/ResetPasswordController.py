from bson import ObjectId
from application.services.reset_password_service import ResetPasswordService
from pydantic import BaseModel
from fastapi import HTTPException, APIRouter, Depends, status
from infrastructure.auth import oauth2
from infrastructure.repositories.mongo_user_repository import MongoUserRepository

router = APIRouter()
reset_password_service = ResetPasswordService()


class ResetPasswordRequestData(BaseModel):
    new_password: str
    repeat_new_password: str


class NotExistentUser(Exception):
    pass


@router.post("/api/v1/reset_password", status_code=status.HTTP_200_OK)
async def reset_password_controller(request: ResetPasswordRequestData, user_id: str = Depends(oauth2.require_user)):
    try:
        mongodb = MongoUserRepository()
        user = mongodb.get_database().find_one({'_id': ObjectId(str(user_id))}) # Oauth2 call maybe should return user not user_id

        if request.new_password == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="new_password field is empty",
            )
        if request.new_password == request.repeat_new_password:
            reset_password_service.reset_password(user_name=user.get("username"), new_password=request.new_password)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password are not matching, try again",
            )
    except NotExistentUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {"message": "Password has been updated successfully"}
