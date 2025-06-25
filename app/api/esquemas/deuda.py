from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class CrearDeudaSchema(BaseModel):
    documento: str = Field(..., description="Numero de documento de identidad del usuario asociado a la deuda", example="10963846374") #type: ignore
    monto: float = Field(..., description="Monto total de la deuda", example=150_000) #type: ignore
    fecha_creacion: Decimal = Field(..., description="Fecha de creación de la deuda en formato ISO 8601 YYYY-MM-DDTHH:MM:SS", examples=["2025-06-24T17:16:00", "2025-06-24"])#type: ignore
    area: str = Field(..., description="Area a la que se asocia la cuenta", example="Tesoreria") #type: ignore
    descripcion: str | None = Field(default=None, description="Detalle del objetivo de la deuda")

    model_config = {"from_attributes": True}


class DeudaRespuestaSchema(BaseModel):
    id: int = Field(..., description="ID único de la deuda", example=123) #type: ignore
    id_usuario: int = Field(..., description="ID del usuario asociado a la deuda", example=45) #type: ignore
    estado: str = Field(..., description="Estado actual de la deuda (ej: 'PENDIENTE', 'PAGADA')", example="PENDIENTE") #type: ignore
    saldo: Decimal = Field(..., description="Saldo restante de la deuda", example=50000.00) #type: ignore
    valor_total: Decimal = Field(..., description="Valor total de la deuda", example=100000.00) #type: ignore
    fecha_creacion: datetime = Field(..., description="Fecha en que se creó la deuda", example="2024-01-01T12:00:00") #type: ignore
    fecha_actualizacion: datetime | None = Field(None, description="Última fecha de actualización", example="2024-06-01T15:30:00") #type: ignore
    id_area: int | None = Field(None, description="ID del área relacionada (si aplica)", example=10) #type: ignore
    descripcion: str | None = Field(None, description="Descripción de la deuda", example="Uniformes") #type: ignore


    model_config = {"from_attributes": True}