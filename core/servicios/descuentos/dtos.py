from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal




@dataclass
class CrearDescuentoDTO:
    id_cuenta_por_pagar: int
    id_usuario: int
    id_deuda: int | None
    valor: Decimal
    fecha_creacion: datetime
    tipo_de_descuento: str
    descripcion: str | None
    fecha_actualizacion: datetime | None