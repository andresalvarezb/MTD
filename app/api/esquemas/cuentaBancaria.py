from pydantic import BaseModel, Field
from datetime import datetime
from .banco import BancoResponseSchema, BancoUpdateSchema


class CuentaBancariaResponseSchema(BaseModel):
    id: int = Field(..., description="Identificador único de la cuenta bancaria")
    id_usuario: int = Field(..., description="ID del usuario al que pertenece la cuenta bancaria")
    numero_certificado: str | None = Field(None, description="Número del certificado bancario asociado")
    numero_cuenta: str = Field(..., description="Número de la cuenta bancaria")
    estado: str = Field(..., description="Estado actual de la cuenta (Ej: ACTIVA, INACTIVA, RECHAZADA)")
    tipo_de_cuenta: str = Field(..., description="Tipo de cuenta (Ej: AHORROS, CORRIENTE)")
    fecha_actualizacion: datetime | None = Field(
        None,
        description="Fecha de la última actualización del registro en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00"],
    )
    observaciones: str | None = Field(None, description="Observaciones o notas adicionales sobre la cuenta bancaria")
    banco: "BancoResponseSchema" = Field(..., description="Información del banco asociado a la cuenta")

    model_config = {"from_attributes": True}


class CuentaBancariaUpdateSchema(BaseModel):
    numero_certificado: str | None = Field(None, description="Número del certificado bancario asociado")
    numero_cuenta: str | None = Field(None, description="Número de la cuenta bancaria")
    estado: str | None = Field(None, description="Estado actual de la cuenta (Ej: ACTIVA, INACTIVA, RECHAZADA)")
    tipo_de_cuenta: str | None = Field(None, description="Tipo de cuenta (Ej: AHORROS, CORRIENTE)")
    observaciones: str | None = Field(None, description="Observaciones o notas adicionales sobre la cuenta bancaria")
    banco: BancoUpdateSchema | None = Field(None, description="Información del banco asociado a la cuenta")

    model_config = {"from_attributes": True}
