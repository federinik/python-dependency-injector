from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide, Closing


class Service:
    init_counter: int = 0
    shutdown_counter: int = 0

    @classmethod
    def reset_counter(cls):
        cls.init_counter = 0
        cls.shutdown_counter = 0

    @classmethod
    def init(cls):
        cls.init_counter += 1

    @classmethod
    def shutdown(cls):
        cls.shutdown_counter += 1


class FactoryService:
    def __init__(self, service: Service):
        self.service = service


class NestedService:
    def __init__(self, factory_service: FactoryService):
        self.factory_service = factory_service


def init_service():
    service = Service()
    service.init()
    yield service
    service.shutdown()


class Container(containers.DeclarativeContainer):

    service = providers.Resource(init_service)
    factory_service = providers.Factory(FactoryService, service)
    factory_service_kwargs = providers.Factory(FactoryService, service=service)
    nested_service = providers.Factory(NestedService, factory_service)


@inject
def test_function(service: Service = Closing[Provide["service"]]):
    return service


@inject
def test_function_dependency(factory: FactoryService = Closing[Provide["factory_service"]]):
    return factory


@inject
def test_function_dependency_kwargs(factory: FactoryService = Closing[Provide["factory_service_kwargs"]]):
    return factory


def test_function_nested_dependency(
    nested: NestedService = Closing[Provide["nested_service"]]
):
    return nested
