"""
Model for endpoint.
"""
from pydantic import BaseModel


class HealthcheckResult(BaseModel):
    is_alive: bool
    date: str
