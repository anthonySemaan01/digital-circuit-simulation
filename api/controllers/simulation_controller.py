import os

from fastapi import APIRouter

from Entities.circuit.circuit import Circuit
from domain.models.simulate_circuit import SimulateCircuit
from shared.helpers.json_handler import read_json_file

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
