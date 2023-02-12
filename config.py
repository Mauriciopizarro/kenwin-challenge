from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str
    FAST_API_PORT: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    CLIENT_ORIGIN: str

    class Config:
        env_file = './.env'


settings = Settings()
