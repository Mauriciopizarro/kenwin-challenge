import random
from domain.interfaces.UserRepository import UserRepository
from domain.models.User import UserPlainPassword, UserDatabaseModel
from infrastructure.Injector import Injector
from domain.interfaces.publisher import Publisher
from dependency_injector.wiring import Provide, inject


class EmptyNewPassword(Exception):
    pass


class ResetPasswordService:

    @inject
    def __init__(
            self, user_repository: UserRepository = Provide[Injector.user_repo],
            publisher: Publisher = Provide[Injector.publisher]
    ):
        self.user_repository = user_repository
        self.publisher = publisher

    def reset_password(self, user_name: str, new_password: str):
        user_db = self.user_repository.get_by_username(user_name)
        user = UserPlainPassword(username=user_db.username, id=user_db.id, plain_password=new_password, email=user_db.email)
        hash_password = user.get_hashed_password()
        updated_user = UserDatabaseModel(username=user_db.username, id=user_db.id, hashed_password=hash_password, email=user_db.email)
        self.user_repository.update_password(updated_user)

        message = {
            "username": user.get_username(),
            "email": user.get_email(),
            "subject": "Password updated successfully"
        }
        self.publisher.send_message(message=message, topic="password_updated_send_email")

    def validate_current_password(self, current_password: str, user_name: str):
        user_db = self.user_repository.get_by_username(user_name)
        user_db.verify_password(current_password)
        return True

    def send_verification_code(self, email):
        code = str(random.randint(1000, 9999))
        message = {
            "email": email,
            "validation_code": code,
            "subject": "Reset password code"
        }
        user = self.user_repository.get_by_email(email)
        user.last_validation_code = code
        self.user_repository.update_verification_last_code(user)
        self.publisher.send_message(message=message, topic="send_reset_password_code_email")

    def compare_codes_and_get_credentials(self, user_email, code):
        user = self.user_repository.get_by_email(user_email)
        user_last_code = user.get_last_validation_code()

        if code == user_last_code:
            return user
        # aca un try catch y retornar una exception en vez de False
        return False
