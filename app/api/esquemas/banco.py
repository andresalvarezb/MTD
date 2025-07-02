from pydantic import BaseModel, Field
from datetime import datetime


class BancoResponseSchema(BaseModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}


class BancoUpdateSchema(BaseModel):
    nombre: str | None = Field(None, description="Nombre de la entidad bancaria")
