import json


def read_json_file(file_path):
    # Load JSON data from file
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def write_json_file(content, file_path):
    with open(file_path, 'w') as file:
        json.dump(content, file, indent=4)
