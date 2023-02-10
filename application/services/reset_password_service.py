from domain.interfaces.UserRepository import UserRepository
from domain.models.User import UserPlainPassword, UserDatabaseModel
from infrastructure.Injector import Injector
from dependency_injector.wiring import Provide, inject


class EmptyNewPassword(Exception):
    pass


class ResetPasswordService:

    @inject
    def __init__(
            self, user_repository: UserRepository = Provide[Injector.user_repo]
    ):
        self.user_repository = user_repository

    def reset_password(self, user_name: str, new_password: str):
        # in a future is posible add old_password and if the old_password is correct, new_password is updated
        if not new_password:
            raise EmptyNewPassword()
        user_db = self.user_repository.get_by_username(user_name, is_user_register=False)
        user = UserPlainPassword(username=user_db.username, id=user_db.id, plain_password=new_password, email=user_db.email)
        hash_password = user.get_hashed_password()
        updated_user = UserDatabaseModel(username=user_db.username, id=user_db.id, hashed_password=hash_password, email=user_db.email)
        self.user_repository.update_password(updated_user)
