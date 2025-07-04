from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class CrearDeudaSchema(BaseModel):
    documento: str = Field(
        ..., description="Numero de documento de identidad del usuario asociado a la deuda", examples=["10963846374"]
    )
    monto: Decimal = Field(..., description="Monto total de la deuda", examples=[150_000])
    fecha_creacion: datetime = Field(
        ...,
        description="Fecha de creación de la deuda en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-24T17:16:00", "2025-06-24"],
    )
    area: str | None = Field(None, description="Nombre del area a la que se asocia la cuenta", examples=["Tesoreria"])
    descripcion: str | None = Field(default=None, description="Detalle del objetivo de la deuda")

    model_config = {"from_attributes": True}


class DeudaRespuestaSchema(BaseModel):
    id: int = Field(..., description="ID único de la deuda", examples=[123])
    id_usuario: int = Field(..., description="ID del usuario asociado a la deuda", examples=[45])
    estado: str = Field(
        ..., description="Estado actual de la deuda (ej: 'PENDIENTE', 'PAGADA')", examples=["PENDIENTE"]
    )
    saldo: Decimal = Field(..., description="Saldo restante de la deuda", examples=[50000.00])
    valor_total: Decimal = Field(..., description="Valor total de la deuda", examples=[100000.00])
    fecha_creacion: datetime = Field(..., description="Fecha en que se creó la deuda", examples=["2024-01-01T12:00:00"])
    fecha_actualizacion: datetime | None = Field(
        None, description="Última fecha de actualización", examples=["2024-06-01T15:30:00"]
    )
    id_area: int | None = Field(None, description="ID del área relacionada (si aplica)", examples=[10])
    descripcion: str | None = Field(None, description="Descripción de la deuda", examples=["Uniformes"])

    model_config = {"from_attributes": True}


class ActualizarDeudaSchema(BaseModel):
    valor_total: Decimal = Field(..., description="Monto total de la deuda", examples=[150_000])
    area: str | None = Field(None, description="Nombre del area a la que se asocia la cuenta", examples=["Tesoreria"])
    descripcion: str | None = Field(default=None, description="Detalle del objetivo de la deuda")
