from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("DEBUG") or os.getenv("DEBUG").lower() == "true":
    load_dotenv("./.env.test")
else:
    load_dotenv("./.env")

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


settings = Settings()
