from application.services.reset_password_service import ResetPasswordService
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import HTTPException, APIRouter, Depends, status, Request, Form
from fastapi.templating import Jinja2Templates
from domain.models.User import IncorrectPasswordError
from infrastructure.auth import oauth2
from infrastructure.exceptions.NotExistentUserException import NotExistentUserException

router = APIRouter()
reset_password_service = ResetPasswordService()
template = Jinja2Templates(directory="./view")


class ResetPasswordRequestData(BaseModel):
    new_password: str
    repeat_new_password: str


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
    user = None
    if reset_password_service.validate_verification_code(user_email, validation_code):
        user = reset_password_service.get_user_after_verification(user_email)

    if user is None:
        return template.TemplateResponse("error.html",
                                         {
                                             "request": req,
                                             "error": 'Error trying to change password, incorrect verification code'
                                         })

    if len(new_pass) > 14 or len(new_pass) < 8:
        return template.TemplateResponse("error.html",
                                         {
                                             "request": req,
                                             "error": 'Error trying to change password, Password should have between 8 and 14 characters'
                                         })

    if new_pass == repeat_new_pass:
        reset_password_service.reset_password(user.get_username(), new_pass)
        return RedirectResponse("/login")

    return template.TemplateResponse("error.html",
                                     {
                                         "request": req,
                                         "error": 'Error trying to change password, try again'
                                     })


@router.post("/send_email_forgot_password", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def reset_password_controller(req: Request, email: str = Form()):
    try:
        reset_password_service.send_verification_code(email)
        return template.TemplateResponse("code_sent.html", {"request": req})
    except NotExistentUserException:
        return template.TemplateResponse("error.html", {"request": req, "error": 'Not existent user to send email'})


# callback from reset_password.html
@router.post("/reset_password", status_code=status.HTTP_200_OK)
async def reset_password_controller(current_password: str = Form(), new_password: str = Form(),
                                    repeat_new_password: str = Form(), user: dict = Depends(oauth2.get_user)):
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
    except NotExistentUserException:
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
async def reset_password_controller(request: ResetPasswordRequestData, user: dict = Depends(oauth2.get_user)):
    try:
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
    except NotExistentUserException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {"message": "Password has been updated successfully"}
