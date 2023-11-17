from typing import Union


class Wire:
    def __init__(self, name: str, has_direct_connection_to_gate: bool = False,
                 direct_connect_to_gate: Union[str, None] = None, seen_as_input_before: bool = False,
                 is_input: bool = False):
        self.name = name
        self.value = False
        self.fanout = []
        self.has_direct_connection_to_gate = has_direct_connection_to_gate
        self.direct_connect_to_gate: Union[str, None] = direct_connect_to_gate
        self.seen_as_input_before: bool = seen_as_input_before
        self.is_input = is_input

    def set_value(self, value):
        self.value = value
        # Propagate the value to all fanout wires/gates
        for fanout_element in self.fanout:
            fanout_element.set_input_value(self.name, value)

    def add_fanout(self, element):
        self.fanout.append(element)

    def __str__(self):
        return f"name: {self.name} || value: {self.value} || fanout: {self.fanout}"
