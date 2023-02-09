from domain.interfaces.UserRepository import UserRepository
from dependency_injector.wiring import Provide, inject
from domain.models.User import UserPlainPassword
from infrastructure.Injector import Injector


class RegisterUserService:

    @inject
    def __init__(
            self, user_repository: UserRepository = Provide[Injector.user_repo]
    ):
        self.user_repository = user_repository

    def register_user(self, email, username, password):
        user = UserPlainPassword(email=email, username=username, plain_password=password)
        response = self.user_repository.save_user(user)
        return {
            "username": response.get_username(),
            "user_id": response.get_id(),
            "email": response.get_email()
        }
