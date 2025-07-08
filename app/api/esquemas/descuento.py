from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from core.entidades.deuda import Deuda
from core.entidades.usuario import Usuario
from core.entidades.cuentaPorPagar import CuentaPorPagar


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


class CrearDescuentoSchema(BaseModel):
    id_cuenta_por_pagar: int
    id_usuario: int
    valor: Decimal
    tipo_de_descuento: str | None
    descripcion: str | None = None
    # fecha_actualizacion: datetime | None = None
    # fecha_creacion: datetime | None = None
    id_deuda: int | None = None


class ActualizarDescuentoSchema(BaseModel):
    valor: Decimal | None = None
    tipo_de_descuento: str | None = None
    descripcion: str | None = None
