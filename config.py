from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    FAST_API_PORT: int
    RABBIT_USERNAME: str
    RABBIT_PASSWORD: str
    RABBIT_HOST: str
    RABBIT_VHOST: str
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str

    class Config:
        env_file = './.env'


settings = Settings()
