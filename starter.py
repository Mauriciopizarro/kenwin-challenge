from fastapi import FastAPI
import infrastructure.Injector # no remove this dependecy
from infrastructure.controllers import RegisterUserController

app = FastAPI()
app.include_router(RegisterUserController.router)
