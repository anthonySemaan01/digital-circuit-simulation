from pydantic import BaseModel
from typing import List, Optional

from domain.models.input_param import InputParam, StuckAt


class SerialSimulation(BaseModel):
    file_name: str
    stuck_at: List[StuckAt] = []
