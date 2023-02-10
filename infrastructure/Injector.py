from dependency_injector import containers, providers
from infrastructure.repositories.mongo_user_repository import MongoUserRepository


class Injector(containers.DeclarativeContainer):
    user_repo = providers.Singleton(MongoUserRepository)


injector = Injector()
injector.wire(modules=["application.services.register_user_service",
                       "application.services.login_service"])
