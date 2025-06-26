from pydantic import BaseModel
from datetime import datetime


class BancoResponseSchema(BaseModel):
    id: int
    nombre: str


    model_config = {"from_attributes": True}