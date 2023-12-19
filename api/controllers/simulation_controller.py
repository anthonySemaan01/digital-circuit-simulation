from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from containers import Services
from domain.contracts.services.abtract_simulation_service import AbstractSimulationService
from domain.models.serial_simulation import SerialSimulation
from domain.models.simulate_circuit import SimulateCircuit

router = APIRouter()


@router.get("/parse_and_build")
@inject
def parse_and_build_circuit(file_name: str,
                            simulation_service: AbstractSimulationService = Depends(
                                Provide[Services.simulation_service])):
    return simulation_service.build_circuit(file_name=file_name)


@router.post("/simulate")
def simulate_circuit(simulate_circuit_params: SimulateCircuit,
                     simulation_service: AbstractSimulationService = Depends(
                         Provide[Services.simulation_service])):
    return simulation_service.simulate(simulate_circuit=simulate_circuit_params)


@router.post("/serial_simulation")
def simulate_circuit(serial_simulation_params: SerialSimulation,
                     simulation_service: AbstractSimulationService = Depends(
                         Provide[Services.simulation_service])):
    return simulation_service.serial_simulation(serial_simulation=serial_simulation_params)
