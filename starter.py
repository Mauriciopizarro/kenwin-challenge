from fastapi import FastAPI
import infrastructure.Injector # no remove this dependecy
from infrastructure.controllers import RegisterUserController, LoginController
import logging.config
import yaml

with open("logging.yaml", 'rt') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
logger.info("Configured the logger!")

app = FastAPI()
app.include_router(RegisterUserController.router)
app.include_router(LoginController.router)
