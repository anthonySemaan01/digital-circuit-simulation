import os
from shared.helpers.json_handler import write_json_file, read_json_file

paths = read_json_file("./assets/paths.json")


def simulate(file_name):
    content_file = None

    with open(os.path.join(paths["benchmarks"], file_name), 'r') as file:
        content_file = file.read()

    return content_file

