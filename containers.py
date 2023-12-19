from dependency_injector import containers, providers

from application.service.simulation_service import SimulationService
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abtract_simulation_service import AbstractSimulationService
from persistance.services.path_service import PathService


class Services(containers.DeclarativeContainer):
    # Singletons
    paths_service = providers.Singleton(AbstractPathService.register(PathService))

    # Application services
    simulation_service = providers.Factory(AbstractSimulationService.register(SimulationService),
                                           path_service=paths_service)
