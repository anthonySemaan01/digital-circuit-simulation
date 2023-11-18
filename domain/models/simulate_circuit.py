from pydantic import BaseModel
from typing import List, Optional

from domain.models.input_param import InputParam, StuckAt


class SimulateCircuit(BaseModel):
    file_name: str
    input_params: List[InputParam]
    stuck_at: StuckAt = None
