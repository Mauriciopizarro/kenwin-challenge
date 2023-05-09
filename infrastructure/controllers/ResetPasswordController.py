from bson import ObjectId
from application.services.reset_password_service import ResetPasswordService
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import HTTPException, APIRouter, Depends, status, Request, Form
from fastapi.templating import Jinja2Templates
from domain.models.User import IncorrectPasswordError, User
from infrastructure.auth import oauth2
from infrastructure.repositories.mongo_user_repository import MongoUserRepository

router = APIRouter()
reset_password_service = ResetPasswordService()
template = Jinja2Templates(directory="./view")


class ResetPasswordRequestData(BaseModel):
    new_password: str
    repeat_new_password: str


class NotExistentUser(Exception):
    pass


# method call from home.html / click in button "change password"
@router.get("/change_password", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def home_controller(req: Request):
    return template.TemplateResponse("reset_password.html", {"request": req})


@router.get("/forgot_password_form", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def home_controller(req: Request):
    return template.TemplateResponse("forgot_password.html", {"request": req})


@router.post("/forgot_password", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def reset_password_controller(req: Request,
                                    validation_code: str = Form(),
                                    new_pass: str = Form(),
                                    repeat_new_pass: str = Form(),
                                    user_email: str = Form()
                                    ):
    user = reset_password_service.compare_codes_and_get_credentials(user_email, validation_code)
    # este user podria ser un false si el verification code es incorrecto, cambiar metodo para que devuelva una exception
    if new_pass == repeat_new_pass:
        reset_password_service.reset_password(user.get_username(), new_pass)
        return RedirectResponse("/login")
    return template.TemplateResponse("error_reset_by_verification_code.html", {"request": req, "error": 'Error on update password, please check the verification code'})


@router.post("/send_email_forgot_password", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def reset_password_controller(req: Request, email: str = Form()):
    reset_password_service.send_verification_code(email)
    return template.TemplateResponse("reset_password_with_code.html", {"request": req, "email": email})


# callback from reset_password.html
@router.post("/reset_password", status_code=status.HTTP_200_OK)
async def reset_password_controller(current_password: str = Form(), new_password: str = Form(), repeat_new_password: str = Form(), user: dict = Depends(oauth2.get_user)):
    try:
        if new_password == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="new_password field is empty",
            )
        if len(new_password) > 14 or len(new_password) < 8:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Password should have between 8 and 14 characters")
        if new_password != repeat_new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password are not matching, try again",
            )
        if reset_password_service.validate_current_password(current_password, user_name=user.get('username')):
            reset_password_service.reset_password(user_name=user.get('username'), new_password=new_password)
    except NotExistentUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except IncorrectPasswordError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect current password",
        )
    return RedirectResponse("/login")


@router.post("/api/v1/reset_password", status_code=status.HTTP_200_OK)
async def reset_password_controller(request: ResetPasswordRequestData, user_id: str = Depends(oauth2.require_user)):
    try:
        mongodb = MongoUserRepository()
        user = mongodb.get_database().find_one({'_id': ObjectId(str(user_id))})  # Oauth2 call maybe should return user not user_id

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
