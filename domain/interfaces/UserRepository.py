from abc import abstractmethod, ABC
from domain.models.User import UserDatabaseModel, UserPlainPassword


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> UserDatabaseModel:
        pass

    @abstractmethod
    def save_user(self, user: UserPlainPassword) -> UserPlainPassword:
        pass

    @abstractmethod
    def update_password(self, user: UserDatabaseModel):
        pass
