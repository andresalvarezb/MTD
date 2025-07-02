from pydantic import BaseModel, Field


class CargoResponseSchema(BaseModel):
    id: int = Field(..., description="Identificador único del cargo o puesto")
    nombre: str = Field(..., description="Nombre del cargo o puesto")

    model_config = {"from_attributes": True}


class CargoUpdateSchema(BaseModel):
    nombre: str | None = Field(None, description="Nombre del cargo o puesto")
