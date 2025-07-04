from pydantic import BaseModel


class CrearAreaMTDSchema(BaseModel):
    nombre: str


class AreaMTDResponseSchema(BaseModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}
