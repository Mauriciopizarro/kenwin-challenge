from abc import abstractmethod, ABC
from domain.models.User import UserDatabaseModel, UserPlainPassword


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str, is_user_register: bool = False) -> UserDatabaseModel:
        pass

    def get_by_email(self, email, is_user_register: bool = False) -> UserDatabaseModel:
        pass

    @abstractmethod
    def save_user(self, user: UserPlainPassword) -> UserPlainPassword:
        pass

    @abstractmethod
    def update_password(self, user: UserDatabaseModel):
        pass

    @abstractmethod
    def update_verification_last_code(self, user: UserDatabaseModel):
        pass
