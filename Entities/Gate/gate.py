import re

from Entities.Wire.wire import Wire


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


def parse_bench_file_with_unique_inputs(file_path):
    circuit = {
        "inputs": [],
        "outputs": [],
        "gates": {},
        "wires": {}
    }

    wires_usage_count: dict = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("INPUT"):
                circuit["inputs"].append(line.split('(')[1].split(')')[0])

            elif line.startswith("OUTPUT"):
                circuit["outputs"].append(line.split('(')[1].split(')')[0])

            else:
                gate_info = line.split('=')

                gate_name = gate_info[0].strip()
                gate_def = gate_info[1].strip()
                gate_type = re.split(r'\(|,', gate_def)[0]

                fanin_names = [fanin_name.strip() for fanin_name in re.findall(r'\(([^)]+)', gate_def)[0].split(',')]

                # for fanin_wire_name in fanin_names:
                #     if fanin_wire_name in wires_usage_count:
                #         wires_usage_count[fanin_wire_name] += 1
                #     else:
                #         wires_usage_count[fanin_wire_name] = 1
                #         circuit["wires"][fanin_wire_name] = Wire(fanin_wire_name)

                fanin_wires = []

                for fanin_wire_name in fanin_names:
                    if fanin_wire_name not in wires_usage_count:
                        wires_usage_count[fanin_wire_name] = 1
                        fanin_wires.append(circuit["wires"][fanin_wire_name])

                    else:
                        new_fanout_wire_name = f"{fanin_wire_name}.{wires_usage_count[fanin_wire_name] - 1}"
                        circuit["wires"][new_fanout_wire_name] = Wire(new_fanout_wire_name)
                        fanin_wires.append(circuit["wires"][new_fanout_wire_name])

                        circuit["wires"][fanin_wire_name].add_fanout(circuit["wires"][new_fanout_wire_name])

                gate = Gate(gate_name, gate_type, fanin_wires)
                circuit["gates"][gate_name] = gate

                output_wire = Wire(gate_name)
                gate.set_output_wire(output_wire)
                circuit["wires"][gate_name] = output_wire

                # for wire in fanin_wires:
                #     wire.add_fanout(gate)
    print(circuit)
    return circuit
