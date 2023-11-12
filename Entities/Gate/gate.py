import re

class Gate:
    def __init__(self, name, gate_type, fanin):
        self.name = name
        self.gate_type = gate_type
        self.fanin = fanin
        self.fanout = []  # Will be populated later based on the circuit

def parse_bench_file(file_path):
    circuit = {
        "inputs": [],
        "outputs": [],
        "gates": {}
    }

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Parse inputs
            if line.startswith("INPUT"):
                input_name = line.split('(')[1].split(')')[0]
                circuit["inputs"].append(input_name)

            # Parse outputs
            elif line.startswith("OUTPUT"):
                output_name = line.split('(')[1].split(')')[0]
                circuit["outputs"].append(output_name)

            # Parse gates
            else:
                gate_info = line.split('=')
                gate_name = gate_info[0].strip()
                gate_def = gate_info[1].strip()
                gate_type = re.split(r'\(|,', gate_def)[0]
                fanin = re.findall(r'\(([^)]+)', gate_def)[0].split(',')
                fanin = [x.strip() for x in fanin]

                circuit["gates"][gate_name] = Gate(gate_name, gate_type, fanin)

    # Populate fanout information
    for gate in circuit["gates"].values():
        for fi in gate.fanin:
            if fi in circuit["gates"]:
                circuit["gates"][fi].fanout.append(gate.name)

    return circuit

# Example usage with a sample file
# parse_bench_file("path_to_bench_file.bench")
# We can't run this code here as it requires a file. You can test it in your environment.


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


def simulate_circuit(circuit, input_vector):
    """
    Simulate the circuit with a given input vector.
    :param circuit: Parsed circuit information.
    :param input_vector: A dictionary mapping input names to their values.
    :return: A dictionary mapping output names to their simulated values.
    """
    # Initialize values for all gates
    values = {name: False for name in circuit["gates"].keys()}

    # Set the input values
    for input_name, value in input_vector.items():
        values[input_name] = value

    # Simulate each gate in levelized order
    for gate_name, gate in circuit["gates"].items():
        gate_inputs = [values[fi] for fi in gate.fanin]
        values[gate_name] = simulate_gate(gate.gate_type, gate_inputs)

    # Extract the output values
    output_values = {output: values[output] for output in circuit["outputs"]}

    return output_values

# Example usage
# circuit_info = parse_bench_file("path_to_bench_file.bench")
# input_vector = {"1": True, "2": False, ... }  # Example input vector
# output_values = simulate_circuit(circuit_info, input_vector)
# The actual values of the input vector depend on the specific circuit and test case.
