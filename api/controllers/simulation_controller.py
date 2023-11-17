import os

from fastapi import APIRouter

from Entities.Gate.gate import parse_bench_file_with_all_unique_wires
from application.service.service.simulation_service import simulate
from shared.helpers.json_handler import read_json_file

paths = read_json_file("./assets/paths.json")

router = APIRouter()


@router.get("/parse_and_build")
def parse_and_build_cirucit(file_name: str):
    data = parse_bench_file_with_all_unique_wires(file_path=os.path.join(paths["benchmarks"], file_name))

    for key, value in data["gates"].items():
        print(f"key: {key} --> {value.toString()}")
    return str(data)


@router.get("/simulate")
def simulate_circuit(file_name: str):
    data = simulate(file_name=file_name)
    return data
