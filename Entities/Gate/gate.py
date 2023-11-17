from Entities.Wire.wire import Wire
import re
class Gate:
    def __init__(self, name, gate_type, fanin_wires):
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


def parse_bench_file_with_wires_and_gates(file_path):
    circuit = {
        "inputs": [],
        "outputs": [],
        "gates": {},
        "wires": {}
    }

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("INPUT"):
                input_name = line.split('(')[1].split(')')[0]
                circuit["inputs"].append(input_name)
                circuit["wires"][input_name] = Wire(input_name)

            elif line.startswith("OUTPUT"):
                output_name = line.split('(')[1].split(')')[0]
                circuit["outputs"].append(output_name)

            else:
                gate_info = line.split('=')
                gate_name = gate_info[0].strip()
                gate_def = gate_info[1].strip()
                gate_type = re.split(r'\(|,', gate_def)[0]
                fanin_names = re.findall(r'\(([^)]+)', gate_def)[0].split(',')
                fanin_wires = [circuit["wires"][name.strip()] for name in fanin_names]

                gate = Gate(gate_name, gate_type, fanin_wires)
                circuit["gates"][gate_name] = gate

                output_wire = Wire(gate_name)
                gate.set_output_wire(output_wire)
                circuit["wires"][gate_name] = output_wire

                for wire in fanin_wires:
                    wire.add_fanout(gate)

    return circuit

# The simulate_circuit function remains the same as simulate_circuit_with_wires
# Example usage:
# circuit_info = parse_bench_file_with_wires_and_gates("path_to_bench_file.bench")
# input_vector = {"1": True, "2": False, ... }
# output_values = simulate_circuit_with_wires(circuit_info, input_vector)
