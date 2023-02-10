from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str
    FAST_API_PORT: int

    class Config:
        env_file = './.env'


settings = Settings()
