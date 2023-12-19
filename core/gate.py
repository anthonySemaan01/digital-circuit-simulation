from typing import List, Union

from core.wire import Wire


class Gate:
    def __init__(self, name: str, gate_type: str, fanin_wires: Union[List[Wire], None] = None,
                 output_wire: Union[Wire, None] = None):
        self.name = name
        self.gate_type = gate_type
        self.fanin_wires = fanin_wires  # List of Wire objects for fanin
        self.output_wire = output_wire  # Will be set later

    def set_output_wire(self, wire):
        self.output_wire = wire

    def get_gate_parameters(self) -> dict:
        fanin_names = [wire.name for wire in self.fanin_wires] if self.fanin_wires else None
        output_wire_name = self.output_wire.name if self.output_wire else None

        return {
            'gate_name': self.name,
            'gate_type': self.gate_type,
            'fanin_wires': fanin_names,
            'output_wire': output_wire_name
        }

    def can_be_triggered(self):
        can_be_triggered = False
        for fanin_wire in self.fanin_wires:
            if not fanin_wire.can_be_triggered:
                return False

        return True

    def simulate(self):

        if self.output_wire.is_stuck_at:
            self.output_wire.value = self.output_wire.stuck_at_value
            self.output_wire.given_a_value = True
            self.output_wire.can_be_triggered = True
            self.output_wire.ensure_fanout_can_be_triggered()

        else:
            values_at_fanin_wires = []

            for input_wire in self.fanin_wires:
                if input_wire.is_stuck_at:
                    values_at_fanin_wires.append(input_wire.stuck_at_value)
                else:
                    values_at_fanin_wires.append(input_wire.value)

            if self.gate_type == "AND":
                value = all(values_at_fanin_wires)
            elif self.gate_type == "NAND":
                value = not all(values_at_fanin_wires)
            elif self.gate_type == "OR":
                value = any(values_at_fanin_wires)
            elif self.gate_type == "NOR":
                value = not any(values_at_fanin_wires)
            elif self.gate_type == "XOR":
                value = sum(values_at_fanin_wires) == 1
            elif self.gate_type == "NOT":
                value = not values_at_fanin_wires[0]
            elif self.gate_type == "XNOR":
                value = not (sum(values_at_fanin_wires))

            self.output_wire.value = value
            self.output_wire.given_a_value = True
            self.output_wire.can_be_triggered = True
            self.output_wire.ensure_fanout_can_be_triggered()
