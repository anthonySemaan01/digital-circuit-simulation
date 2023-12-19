import copy
import os
import time
from typing import List

from core.circuit import Circuit
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abtract_simulation_service import AbstractSimulationService
from domain.models.input_param import InputParam
from domain.models.serial_simulation import SerialSimulation
from domain.models.simulate_circuit import SimulateCircuit


class SimulationService(AbstractSimulationService):
    def __init__(self, path_service: AbstractPathService):
        self.path_service = path_service

    def simulate(self, simulate_circuit: SimulateCircuit):
        circuit = Circuit()
        if simulate_circuit.file_name not in os.listdir(self.path_service.paths.benchmarks):
            raise Exception("Filename not available")
        circuit.parse_bench_file_with_unique_inputs(
            file_path=os.path.join(self.path_service.paths.benchmarks, simulate_circuit.file_name))
        circuit.simulate_circuit(input_vector=simulate_circuit.input_params, place_stuck_at=simulate_circuit.stuck_at)

        circuit_output_values = circuit.get_circuit_output_values()
        wires = circuit.wires

        wires_values = {}
        for wire in wires:
            wires_values[wire.name] = wire.value

        return {
            "circuit_output_values": circuit_output_values,
            "wires_values": wires_values
        }

    def serial_simulation(self, serial_simulation: SerialSimulation):
        start = time.time()
        number_of_detected_faults = 0
        circuit = Circuit()
        if serial_simulation.file_name not in os.listdir(self.path_service.paths.benchmarks):
            raise Exception("Filename not available")
        circuit.parse_bench_file_with_unique_inputs(
            file_path=os.path.join(self.path_service.paths.benchmarks, serial_simulation.file_name))

        input_patterns = circuit.generate_wire_patterns()
        new_input_patterns = []
        for index, input_pattern in enumerate(input_patterns):
            new_input_patterns.append({index: input_pattern})

        # Get true value simulation
        circuit_results_per_input_pattern = {}
        for index, input_pattern in enumerate(new_input_patterns):
            input_parameters: List[InputParam] = []

            for input_name, input_value in input_pattern[index].items():
                input_parameters.append(InputParam(wire_name=input_name, value=input_value))

            copy_of_circuit = copy.deepcopy(circuit)
            copy_of_circuit.simulate_circuit(input_vector=input_parameters)
            circuit_results_per_input_pattern[index] = copy_of_circuit.get_circuit_output_values()

        faults_detected = []
        for stuck_at_fault in serial_simulation.stuck_at:
            for index, input_pattern in enumerate(new_input_patterns):
                # have the input parameter list compatible with simulate circuit
                input_parameters: List[InputParam] = []
                for input_name, input_value in input_pattern[index].items():
                    input_parameters.append(InputParam(wire_name=input_name, value=input_value))

                copy_of_circuit = copy.deepcopy(circuit)
                copy_of_circuit.simulate_circuit(input_vector=input_parameters, place_stuck_at=stuck_at_fault)
                circuit_output = copy_of_circuit.get_circuit_output_values()

                if circuit_output != circuit_results_per_input_pattern[index]:
                    faults_detected.append({"fault": stuck_at_fault,
                                            "vector_used": input_parameters,
                                            "true_value": circuit_results_per_input_pattern[index],
                                            "faulty_value": circuit_output})
                    number_of_detected_faults += 1
                    break

        end = time.time()
        return {
            "input_patterns": new_input_patterns,
            "simulation_results": circuit_results_per_input_pattern,
            "faults_detected": faults_detected,
            "total_time": end - start,
            "fault_coverage": number_of_detected_faults / len(serial_simulation.stuck_at),
            "fault_efficiency": number_of_detected_faults / (
                    len(serial_simulation.stuck_at) + len(serial_simulation.stuck_at) - number_of_detected_faults)
        }

    def build_circuit(self, file_name: str):
        circuit = Circuit()
        if file_name not in os.listdir(self.path_service.paths.benchmarks):
            raise Exception("Filename not available")
        circuit.parse_bench_file_with_unique_inputs(
            file_path=os.path.join(self.path_service.paths.benchmarks, file_name))

        return {
            "inputs": [wire.get_wire_parameters() for wire in circuit.inputs],
            "all_wires": [wire.get_wire_parameters() for wire in circuit.wires],
            "all_gates": [gate.get_gate_parameters() for gate in circuit.gates],
            "outputs": [wire.get_wire_parameters() for wire in circuit.outputs]
        }
