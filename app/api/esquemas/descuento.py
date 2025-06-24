from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class DescuentoResponseSchema(BaseModel):
    id_cuenta_por_pagar: int
    id_usuario: int
    valor: Decimal
    fecha_creacion: datetime
    tipo_de_descuento: str
    id_deuda: int | None
    id: int | None
    descripcion: str | None
    fecha_actualizacion: datetime | None

    model_config = {"from_attributes": True}
