from dependency_injector import containers, providers
from infrastructure.repositories.mongo_task_repository import MongoTaskRepository
from infrastructure.repositories.mongo_user_repository import MongoUserRepository


class Injector(containers.DeclarativeContainer):
    user_repo = providers.Singleton(MongoUserRepository)
    task_repo = providers.Singleton(MongoTaskRepository)


injector = Injector()
injector.wire(modules=["application.services.register_user_service",
                       "application.services.login_service",
                       "application.services.reset_password_service",
                       "application.services.create_task_service",
                       "application.services.get_task_service",
                       "application.services.finish_task_service"
                       ])
