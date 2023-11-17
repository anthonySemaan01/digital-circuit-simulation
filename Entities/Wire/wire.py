class Wire:
    def __init__(self, name):
        self.name = name
        self.value = False
        self.fanout = []

    def set_value(self, value):
        self.value = value
        # Propagate the value to all fanout wires/gates
        for fanout_element in self.fanout:
            fanout_element.set_input_value(self.name, value)

    def add_fanout(self, element):
        self.fanout.append(element)

    def __str__(self):
        return f"name: {self.name} || value: {self.value} || fanout: {self.fanout}"
