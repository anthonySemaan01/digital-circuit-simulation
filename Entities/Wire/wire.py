from typing import Union, List


class Wire:
    def __init__(self, name: str, has_direct_connection_to_gate: bool = False,
                 direct_connect_to_gate: Union[str, None] = None, seen_as_input_before: bool = False,
                 is_input: bool = False, is_stuck_at: bool = False, stuck_at_value: Union[None, bool] = None,
                 can_be_triggered: bool = False, value: bool = False, given_a_value: bool = False):
        self.name = name
        self.value = value
        self.given_a_value = given_a_value
        self.fanout: List[Wire] = []
        self.has_direct_connection_to_gate = has_direct_connection_to_gate
        self.direct_connect_to_gate: Union[str, None] = direct_connect_to_gate
        self.seen_as_input_before: bool = seen_as_input_before
        self.is_input = is_input
        self.is_stuck_at = is_stuck_at
        self.stuck_at_value = stuck_at_value
        self.can_be_triggered = False

    def ensure_fanout_can_be_triggered(self):
        if self.can_be_triggered:
            for fanout_wire in self.fanout:
                fanout_wire.ensure_fanout_can_be_triggered()  # Recursively call for each fanout wire
                fanout_wire.can_be_triggered = True

                if not fanout_wire.given_a_value:  # Check if fanout wire already has a value
                    if fanout_wire.is_stuck_at:
                        fanout_wire.value = self.stuck_at_value
                    else:
                        fanout_wire.value = self.value
                    fanout_wire.given_a_value = True  # Mark fanout wire as given a value

                    fanout_wire.ensure_fanout_can_be_triggered()  # Recursively assign value to fanout wires

    def __str__(self):
        return f"name: {self.name} || value: {self.value} || given a value: {self.given_a_value} || can_be_triggered: {self.can_be_triggered} || fanout: {[str(wire) for wire in self.fanout]}"

    def get_wire_parameters(self) -> dict:
        return {
            'name': self.name,
            'value': self.value,
            'given_a_value': self.given_a_value,
            'fanout': [wire.name for wire in self.fanout],  # Extracting names of fanout wires for readability
            'has_direct_connection_to_gate': self.has_direct_connection_to_gate,
            'direct_connect_to_gate': self.direct_connect_to_gate,
            'seen_as_input_before': self.seen_as_input_before,
            'is_input': self.is_input,
            'is_stuck_at': self.is_stuck_at,
            'stuck_at_value': self.stuck_at_value,
            'can_be_triggered': self.can_be_triggered
        }