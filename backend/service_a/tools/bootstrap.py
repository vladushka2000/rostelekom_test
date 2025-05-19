from repositories import eqp_repository
from services import configurator_service


class Bootstrap:
    """
    DI-контейнер на минималках
    """

    repo = eqp_repository.EqpRepository()
    service = configurator_service.ConfiguratorService()
