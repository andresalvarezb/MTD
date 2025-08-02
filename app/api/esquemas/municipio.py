from pydantic import BaseModel, Field
from .departamento import DepartamentoResponseSchema, DepartamentoUpdateSchema


class MunicipioCreateSchema(BaseModel):
    nombre: str = Field(..., description="Nombre del municipio", examples=["Medellín"])
    departamento: DepartamentoUpdateSchema = Field(..., description="Departamento al que pertenece el municipio", examples=["Antioquia"])


class MunicipioResponseSchema(BaseModel):
    id: int = Field(..., description="Identificador único del municipio")
    nombre: str = Field(..., description="Nombre del municipio")
    departamento: DepartamentoResponseSchema = Field(..., description="Departamento al que pertenece el municipio")

    model_config = {"from_attributes": True}


class MunicipioUpdateSchema(BaseModel):
    nombre: str | None = Field(None, description="Nombre del municipio")
    # departamento: DepartamentoUpdateSchema | None = Field(None, description="Departamento al que pertenece el municipio")

    model_config = {"from_attributes": True}
