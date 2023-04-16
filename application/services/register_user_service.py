from domain.interfaces.UserRepository import UserRepository
from dependency_injector.wiring import Provide, inject
from domain.interfaces.publisher import Publisher
from domain.models.User import UserPlainPassword
from infrastructure.Injector import Injector
from infrastructure.exceptions.InvalidMinCharactersPasswordException import InvalidMinCharactersPasswordException


class RegisterUserService:

    @inject
    def __init__(
            self, user_repository: UserRepository = Provide[Injector.user_repo],
            publisher: Publisher = Provide[Injector.publisher]
    ):
        self.user_repository = user_repository
        self.publisher = publisher

    def register_user(self, email, username, password):
        if 8 > len(password) or len(password) > 14:
            raise InvalidMinCharactersPasswordException()

        user = UserPlainPassword(email=email, username=username, plain_password=password)
        self.user_repository.get_by_email(email, True)
        self.user_repository.get_by_username(username, True)
        response = self.user_repository.save_user(user)

        message = {
            "username": user.get_username(),
            "email": user.get_email(),
            "subject": "User has been successfully created"
        }
        self.publisher.send_message(message=message, topic='user_created_send_email')

        return {
            "username": response.get_username(),
            "user_id": response.get_id(),
            "email": response.get_email()
        }
