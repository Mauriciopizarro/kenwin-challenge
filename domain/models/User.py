from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):

    username: str
    email: EmailStr
    id: Optional[str]

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def set_id(self, user_id: str):
        self.id = user_id

    def set_username(self, username: str):
        self.username = username

    def set_email(self, email: EmailStr):
        self.email = email


class UserDatabaseModel(User):
    hashed_password: str

    def get_hashed_password(self):
        return self.hashed_password

    def verify_password(self, plain_password):
        if not pwd_context.verify(plain_password, self.hashed_password):
            raise IncorrectPasswordError


class UserPlainPassword(User):
    plain_password: constr(min_length=8)

    def get_plain_password(self):
        return self.plain_password

    def get_hashed_password(self):
        return pwd_context.hash(self.plain_password)


class IncorrectPasswordError(Exception):
    pass


class EmptyPasswordError(Exception):
    pass
