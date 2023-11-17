from Entities.Wire.wire import Wire
import re
class Gate:
    def __init__(self, name, gate_type, fanin_wires):
        self.name = name
        self.gate_type = gate_type
        self.fanin_wires = list(map(lambda x: x.toString(), fanin_wires)) # List of Wire objects for fanin
        self.output_wire = None  # Will be set later

    def set_output_wire(self, wire):
        self.output_wire = wire.toString()

    def compute_output(self):
        input_values = [wire.value for wire in self.fanin_wires]
        output_value = simulate_gate(self.gate_type, input_values)
        if self.output_wire:
            self.output_wire.set_value(output_value)

    def toString(self):
        return self.name,self.gate_type,self.fanin_wires,self.output_wire


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
def parse_bench_file_with_all_unique_wires(file_path):
    circuit = {
        "inputs": [],
        "outputs": [],
        "gates": {},
        "wires": {}
    }
    wire_usage_count = {}  # Track how many times each wire is used

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("INPUT"):
                input_name = line.split('(')[1].split(')')[0]
                circuit["inputs"].append(input_name)
                circuit["wires"][input_name] = Wire(input_name)
                wire_usage_count[input_name] = 0

            elif line.startswith("OUTPUT"):
                output_name = line.split('(')[1].split(')')[0]
                circuit["outputs"].append(output_name)

            else:
                gate_info = line.split('=')
                gate_name = gate_info[0].strip()
                gate_def = gate_info[1].strip()
                gate_type = re.split(r'\(|,', gate_def)[0]
                fanin_names = re.findall(r'\(([^)]+)', gate_def)[0].split(',')

                fanin_wires = []
                for name in fanin_names:
                    name = name.strip()
                    wire_usage_count.setdefault(name, 0)
                    wire_usage_count[name] += 1
                    new_name = f"{name}.{wire_usage_count[name]}"
                    new_name2 = f"{name}.{wire_usage_count[name]-1}"
                    if wire_usage_count[name] >=2:
                        circuit["wires"][new_name] = Wire(new_name)
                        fanin_wires.append(circuit["wires"][new_name])

                        circuit["wires"][new_name2] = Wire(new_name2)
                        fanin_wires.append(circuit["wires"][new_name2])
                        if name in circuit["wires"]:
                            circuit["wires"][name].add_fanout(circuit["wires"][new_name])
                            circuit["wires"][name].add_fanout(circuit["wires"][new_name2])

                gate = Gate(gate_name, gate_type, fanin_wires)
                circuit["gates"][gate_name] = gate

                output_wire = Wire(gate_name)
                gate.set_output_wire(output_wire)
                circuit["wires"][gate_name] = output_wire

                for wire in fanin_wires:
                    wire.add_fanout(gate)
    print(circuit["wires"])
    return circuit

# The simulate_circuit function remains the same as simulate_circuit_with_wires
# Example usage:
circuit_info = parse_bench_file_with_all_unique_wires("../../data/benchmarks/c17.txt")
# input_vector = {"1": True, "2": False, ... }
# output_values = simulate_circuit_with_wires(circuit_info, input_vector)
