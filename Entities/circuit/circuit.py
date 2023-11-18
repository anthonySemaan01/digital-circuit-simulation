import re
from typing import List, Union

from Entities.Gate.gate import Gate
from Entities.Wire.wire import Wire


class Circuit:
    def __init__(self):
        self.inputs: List[Wire] = []
        self.outputs: List[Wire] = []
        self.gates: List[Gate] = []
        self.wires: List[Wire] = []

    def get_all_wires_names(self):
        wires_names = []
        for wire in self.wires:
            wires_names.append(wire.name)

        return wires_names

    def get_wire_based_on_name(self, name: str):
        for index, wire in enumerate(self.wires):
            if name == wire.name:
                return wire

        return None

    def get_gate_by_name(self, name: str):
        for index, gate in enumerate(self.gates):
            if name == gate.name:
                return gate

        return None

    def parse_bench_file_with_unique_inputs(self, file_path: str):
        wires_usage_count: dict = {}

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.startswith("INPUT"):
                    new_input_wire = Wire(name=line.split('(')[1].split(')')[0], is_input=True,
                                          seen_as_input_before=False, has_direct_connection_to_gate=False)
                    self.inputs.append(new_input_wire)
                    self.wires.append(new_input_wire)

                elif line.startswith("OUTPUT"):
                    new_output_wire = Wire(name=line.split('(')[1].split(')')[0], is_input=True,
                                           seen_as_input_before=False, has_direct_connection_to_gate=False)
                    self.outputs.append(new_output_wire)
                    self.wires.append(new_output_wire)

                else:
                    gate_info = line.split('=')

                    gate_name = gate_info[0].strip()
                    gate_def = gate_info[1].strip()
                    gate_type = re.split(r'\(|,', gate_def)[0]

                    created_gate = Gate(name=gate_name, gate_type=gate_type)

                    fanin_names = [fanin_name.strip() for fanin_name in
                                   re.findall(r'\(([^)]+)', gate_def)[0].split(',')]

                    fanin_wires_for_that_specific_gate = []

                    for fanin_wire_name in fanin_names:
                        wire: Union[Wire, None] = None

                        if fanin_wire_name in self.get_all_wires_names():
                            wire = self.get_wire_based_on_name(fanin_wire_name)

                            if wire.seen_as_input_before:
                                if len(wire.fanout) == 0:
                                    wire_one = Wire(name=f"{fanin_wire_name}.{len(wire.fanout) + 1}",
                                                    seen_as_input_before=True,
                                                    direct_connect_to_gate=self.get_gate_by_name(
                                                        wire.direct_connect_to_gate),
                                                    has_direct_connection_to_gate=True)
                                    wire.fanout.append(wire_one)

                                    wire_two = Wire(name=f"{fanin_wire_name}.{len(wire.fanout) + 1}",
                                                    seen_as_input_before=True,
                                                    direct_connect_to_gate=self.get_gate_by_name(
                                                        wire.direct_connect_to_gate),
                                                    has_direct_connection_to_gate=True)
                                    wire.fanout.append(wire_two)

                                    fanin_wires_for_that_specific_gate.append(wire_two)

                                    wire.has_direct_connection_to_gate = False
                                    wire.direct_connect_to_gate = None

                                    self.wires.append(wire_one)
                                    self.wires.append(wire_two)
                                else:
                                    additional_wire = Wire(name=f"{fanin_wire_name}.{len(wire.fanout) + 1}",
                                                           seen_as_input_before=True,
                                                           direct_connect_to_gate=created_gate.name,
                                                           has_direct_connection_to_gate=True)
                                    wire.fanout.append(additional_wire)
                                    self.wires.append(additional_wire)
                                    fanin_wires_for_that_specific_gate.append(additional_wire)

                            else:
                                wire.direct_connect_to_gate = created_gate.name
                                wire.has_direct_connection_to_gate = True
                                wire.seen_as_input_before = True

                                fanin_wires_for_that_specific_gate.append(wire)
                        else:
                            wire = Wire(name=fanin_wire_name,
                                        seen_as_input_before=True,
                                        has_direct_connection_to_gate=True,
                                        direct_connect_to_gate=created_gate.name)
                            self.wires.append(wire)
                            fanin_wires_for_that_specific_gate.append(wire)

                    created_gate.fanin_wires = fanin_wires_for_that_specific_gate

                    created_output_wire = Wire(name=created_gate.name, has_direct_connection_to_gate=False,
                                               seen_as_input_before=False)
                    created_gate.output_wire = created_output_wire
                    self.wires.append(created_output_wire)
                    self.gates.append(created_gate)

    def __str__(self):
        return f"inputs: {[str(wire) for wire in self.inputs]} || outputs: {[str(wire) for wire in self.outputs]} || gates: {[str(gate) for gate in self.gates]} || wires: {[str(wire) for wire in self.wires]}"
