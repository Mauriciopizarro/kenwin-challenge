from domain.interfaces.UserRepository import UserRepository
from infrastructure.Injector import Injector
from dependency_injector.wiring import Provide, inject


class LoginService:

    @inject
    def __init__(
            self, user_repository: UserRepository = Provide[Injector.user_repo]
    ):
        self.user_repository = user_repository

    def login(self, email: str, password: str):
        user = self.user_repository.get_by_email(email=email)
        user.verify_password(password)
        return user
