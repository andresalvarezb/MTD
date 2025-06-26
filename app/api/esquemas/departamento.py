from pydantic import BaseModel
from datetime import datetime


class DepartamentoResponseSchema(BaseModel):
    id: int
    nombre: str


    model_config = {"from_attributes": True}