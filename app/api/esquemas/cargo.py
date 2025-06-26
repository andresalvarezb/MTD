from pydantic import BaseModel


class CargoResponseSchema(BaseModel):
    id: int
    nombre: str


    model_config = {"from_attributes": True}