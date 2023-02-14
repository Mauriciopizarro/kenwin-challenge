import infrastructure.Injector # no remove this dependecy
from infrastructure.controllers import \
    RegisterUserController, \
    AuthController, \
    ResetPasswordController, \
    CreateTaskController, \
    GetTaskController, \
    FinishTaskController
from fastapi import FastAPI
import logging.config
import yaml


with open("logging.yaml", 'rt') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
logger.info("Configured the logger!")

app = FastAPI()

app.include_router(RegisterUserController.router)
app.include_router(AuthController.router)
app.include_router(ResetPasswordController.router)
app.include_router(CreateTaskController.router)
app.include_router(GetTaskController.router)
app.include_router(FinishTaskController.router)
