from pydantic import BaseModel


class InputParam(BaseModel):
    wire_name: str
    value: bool


class StuckAt(BaseModel):
    wire_name: str
    value: bool
