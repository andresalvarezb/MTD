from pydantic import BaseModel, Field
from datetime import datetime
from .usuario import UsuarioResponseSchema
from .municipio import MunicipioResponseSchema
from .cargo import CargoResponseSchema


# class HistorialLaboralResponseSchema(BaseModel):
#     id: int
#     claveHLU: str
#     contrato: str
#     seguridad_social: bool
#     fecha_contratacion: str
#     fecha_fin_contratacion: str
#     fecha_aprobacion_seguridad_social: str
#     fecha_ultima_contratacion: str
#     usuario: UsuarioResponseSchema
#     municipio: MunicipioResponseSchema
#     cargo: CargoResponseSchema

#     model_config = {"from_attributes": True}


class HistorialLaboralResponseSchema(BaseModel):
    id: int = Field(..., description="Identificador único del historial laboral")
    claveHLU: str = Field(
        ...,
        description="Clave interna del historial laboral del usuario (HLU). Es la union del mesdeservicio-documento-mesradicacioncontable",
        examples=["20250501110677908520250601"],
    )
    contrato: str = Field(..., description="Tipo del contrato asociado")
    seguridad_social: bool = Field(..., description="Indica si el trabajador está afiliado a seguridad social")
    fecha_contratacion: datetime| None = Field(None, description="Fecha en que inició la contratación (formato ISO 8601) YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"])
    fecha_fin_contratacion: datetime | None = Field(None, description="Fecha en que terminó la contratación (formato ISO 8601) YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"])
    fecha_aprobacion_seguridad_social: datetime | None = Field(
        None, description="Fecha de aprobación de la afiliación a la seguridad social (formato ISO 8601) YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"]
    )
    fecha_ultima_contratacion: datetime| None = Field(None, description="Fecha de la última contratación del usuario (formato ISO 8601) YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"]
    )
    usuario: UsuarioResponseSchema = Field(..., description="Información del usuario asociado")
    municipio: MunicipioResponseSchema = Field(..., description="Municipio relacionado con el historial laboral")
    cargo: CargoResponseSchema = Field(..., description="Cargo o puesto desempeñado por el usuario")

    model_config = {"from_attributes": True}