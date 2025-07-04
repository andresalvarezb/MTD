from pydantic import BaseModel, Field


class DepartamentoResponseSchema(BaseModel):
    id: int = Field(..., description="Identificador único del departamento")
    nombre: str = Field(..., description="Nombre del departamento")

    model_config = {"from_attributes": True}


class DepartamentoUpdateSchema(BaseModel):
    nombre: str | None = Field(None, description="Nombre del departamento")
