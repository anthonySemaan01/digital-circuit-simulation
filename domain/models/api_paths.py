import os

from pydantic import BaseModel, validator


class ApiPaths(BaseModel):
    benchmarks: str
