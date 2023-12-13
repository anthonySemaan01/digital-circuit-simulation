import os

from fastapi import APIRouter

from Entities.circuit.circuit import Circuit
from domain.models.simulate_circuit import SimulateCircuit
from domain.models.serial_simulation import SerialSimulation
from shared.helpers.json_handler import read_json_file
from domain.models.input_param import InputParam
from typing import List, Dict

paths = read_json_file("./assets/paths.json")

router = APIRouter()


@router.get("/parse_and_build")
def parse_and_build_circuit(file_name: str):
    # data = parse_bench_file_with_unique_inputs(file_path=os.path.join(paths["benchmarks"], file_name))

    circuit = Circuit()
    circuit.parse_bench_file_with_unique_inputs(file_path=os.path.join(paths["benchmarks"], file_name))
    inputs = circuit.inputs
    inputs = [wire.get_wire_parameters() for wire in inputs]

    all_wires = circuit.wires
    all_wires = [wire.get_wire_parameters() for wire in all_wires]

    all_gates = circuit.gates
    all_gates = [gate.get_gate_parameters() for gate in all_gates]

    outputs = circuit.outputs
    outputs = [wire.get_wire_parameters() for wire in outputs]

    return {
        "inputs": inputs,
        "all_wires": all_wires,
        "all_gates": all_gates,
        "outputs": outputs
    }


@router.post("/simulate")
def simulate_circuit(simulate_circuit: SimulateCircuit):
    circuit = Circuit()
    circuit.parse_bench_file_with_unique_inputs(file_path=os.path.join(paths["benchmarks"], simulate_circuit.file_name))
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


@router.post("/serial_simulation")
def simulate_circuit(serial_simulation: SerialSimulation):
    circuit = Circuit()
    circuit.parse_bench_file_with_unique_inputs(
        file_path=os.path.join(paths["benchmarks"], serial_simulation.file_name))

    input_patterns = circuit.generate_wire_patterns()
    new_input_patterns = []
    for index, input_pattern in enumerate(input_patterns):
        new_input_patterns.append({index: input_pattern})

    circuit_results_per_input_pattern = {}
    for index, input_pattern in enumerate(new_input_patterns):
        input_parameters: List[InputParam] = []

        for input_name, input_value in input_pattern[index].items():
            input_parameters.append(InputParam(wire_name=input_name, value=input_value))

        copy_of_circuit = circuit
        copy_of_circuit.simulate_circuit(input_vector=input_parameters)
        circuit_results_per_input_pattern[index] = copy_of_circuit.get_circuit_output_values()

    return {
        "input_patterns": new_input_patterns,
        "simulation_results": circuit_results_per_input_pattern
    }
