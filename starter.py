import infrastructure.Injector # no remove this dependecy
from config import settings
from infrastructure.controllers import \
    RegisterUserController, \
    AuthController, \
    ResetPasswordController, \
    CreateTaskController, \
    GetTaskController, FinishTaskController
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import logging.config
import yaml


with open("logging.yaml", 'rt') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
logger.info("Configured the logger!")

origins = [
    settings.CLIENT_ORIGIN,
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(RegisterUserController.router)
app.include_router(AuthController.router)
app.include_router(ResetPasswordController.router)
app.include_router(CreateTaskController.router)
app.include_router(GetTaskController.router)
app.include_router(FinishTaskController.router)
