from domain.interfaces.UserRepository import UserRepository
from domain.models.User import UserDatabaseModel, UserPlainPassword


class MockUserRepository(UserRepository):

    def __init__(self, user=None):
        self.user = user

    def get_by_username(self, username: str, is_user_register: bool = False) -> UserDatabaseModel:
        return self.user

    def get_by_email(self, email, is_user_register: bool = False) -> UserDatabaseModel:
        return self.user

    def save_user(self, user: UserPlainPassword) -> UserPlainPassword:
        return user

    def update_password(self, user: UserDatabaseModel):
        pass
