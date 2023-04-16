import infrastructure.Injector
# Don't remove injector dependency
from infrastructure.events.rabbit_connection import RabbitConnection
import logging.config
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
import time


with open("logging.yaml", 'rt') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
logger.info("Configured the logger!")

time.sleep(5)
queues = ["password_updated_send_email", "user_created_send_email"]
channel = RabbitConnection.get_channel()
RabbitConnection.declare_queues(channel, queues)

app = FastAPI()

app.include_router(RegisterUserController.router)
app.include_router(AuthController.router)
app.include_router(ResetPasswordController.router)
app.include_router(CreateTaskController.router)
app.include_router(GetTaskController.router)
app.include_router(FinishTaskController.router)
