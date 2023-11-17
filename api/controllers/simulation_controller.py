from fastapi import APIRouter
from starlette.responses import Response
from application.service.service.simulation_service import simulate

router = APIRouter()


@router.get("/simulate")
def simulate_circuit(file_name: str):
    data = simulate(file_name=file_name)
    return data
