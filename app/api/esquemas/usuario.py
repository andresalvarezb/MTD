from pydantic import BaseModel, Field
from datetime import datetime
from .municipio import MunicipioResponseSchema, MunicipioUpdateSchema
from .cargo import CargoResponseSchema, CargoUpdateSchema


# class UsuarioResponseSchema(BaseModel):
#     id: int
#     documento: str
#     nombre: str
#     estado: str
#     contrato: str
#     correo: str
#     telefono: str
#     seguridad_social: bool
#     fecha_ultima_contratacion: datetime
#     fecha_aprobacion_seguridad_social: datetime
#     cargo: CargoResponseSchema
#     municipio: MunicipioResponseSchema


#     model_config = {"from_attributes": True}


class UsuarioResponseSchema(BaseModel):
    id: int = Field(..., description="Identificador único del usuario")
    documento: str = Field(..., description="Número de documento del usuario")
    nombre: str = Field(..., description="Nombre completo del usuario")
    estado: str = Field(..., description="Estado actual del usuario (activo, inactivo, etc.)")
    contrato: str = Field(..., description="Tipo o número de contrato del usuario")
    correo: str = Field(..., description="Correo electrónico de contacto")
    telefono: str = Field(..., description="Número de teléfono de contacto")
    seguridad_social: bool = Field(..., description="Indica si el usuario está afiliado a seguridad social")
    fecha_ultima_contratacion: datetime | None = Field(
        None,
        description="Fecha de la última contratación del usuario (formato ISO 8601) YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_aprobacion_seguridad_social: datetime | None = Field(
        None,
        description="Fecha en que se aprobó la afiliación a seguridad social (formato ISO 8601) YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    cargo: CargoResponseSchema = Field(..., description="Cargo que desempeña el usuario")
    municipio: MunicipioResponseSchema = Field(..., description="Municipio asociado al usuario")

    model_config = {"from_attributes": True}


class UsuarioUpdateSchema(BaseModel):
    documento: str | None = Field(None, description="Número de documento del usuario")
    nombre: str | None = Field(None, description="Nombre completo del usuario")
    estado: str | None = Field(None, description="Estado actual del usuario (activo, inactivo, etc.)")
    contrato: str | None = Field(None, description="Tipo o número de contrato del usuario")
    correo: str | None = Field(None, description="Correo electrónico de contacto")
    telefono: str | None = Field(None, description="Número de teléfono de contacto")

    model_config = {"from_attributes": True}
