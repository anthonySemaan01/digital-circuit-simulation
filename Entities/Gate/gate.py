from typing import List, Union
from Entities.Wire.wire import Wire


class Gate:
    def __init__(self, name: str, gate_type: str, fanin_wires: List[Wire]):
        self.name = name
        self.gate_type = gate_type
        self.fanin_wires = fanin_wires  # List of Wire objects for fanin
        self.output_wire = None  # Will be set later

    def set_output_wire(self, wire):
        self.output_wire = wire

    def compute_output(self):
        input_values = [wire.value for wire in self.fanin_wires]
        output_value = simulate_gate(self.gate_type, input_values)
        if self.output_wire:
            self.output_wire.set_value(output_value)

    def __str__(self):
        return f"name: {self.name} || gate_type: {self.gate_type} || fan_in: {self.fanin_wires} || fan_out: {self.output_wire}"





def simulate_gate(gate_type, inputs):
    """
    Simulate the logic of a gate.
    :param gate_type: Type of the gate (e.g., AND, NAND, OR, etc.)
    :param inputs: Input values for the gate.
    :return: Output of the gate.
    """
    if gate_type == "AND":
        return all(inputs)
    elif gate_type == "NAND":
        return not all(inputs)
    elif gate_type == "OR":
        return any(inputs)
    elif gate_type == "NOR":
        return not any(inputs)
    elif gate_type == "XOR":
        return sum(inputs) == 1
    elif gate_type == "INVERTER":
        return not inputs[0]
    else:
        raise ValueError(f"Unknown gate type: {gate_type}")
