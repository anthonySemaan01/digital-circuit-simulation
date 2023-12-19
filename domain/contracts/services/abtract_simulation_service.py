from abc import ABC, ABCMeta, abstractmethod
from typing import Dict

from domain.models.serial_simulation import SerialSimulation
from domain.models.simulate_circuit import SimulateCircuit


class AbstractSimulationService(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def build_circuit(self, file_name: str) -> Dict: raise NotImplementedError

    @abstractmethod
    def simulate(self, simulate_circuit: SimulateCircuit) -> Dict: raise NotImplementedError

    @abstractmethod
    def serial_simulation(self, serial_simulation: SerialSimulation) -> Dict: raise NotImplementedError
