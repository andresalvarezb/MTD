from pydantic import BaseModel
from .departamento import DepartamentoResponseSchema


class MunicipioResponseSchema(BaseModel):
    id: int
    nombre: str
    departamento: DepartamentoResponseSchema

    model_config = {"from_attributes": True}
