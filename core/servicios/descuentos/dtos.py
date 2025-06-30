from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from core.entidades.deuda import Deuda
from core.entidades.usuario import Usuario
from core.entidades.cuentaPorPagar import CuentaPorPagar


@dataclass
class CrearDescuentoDTO:
    cuenta_por_pagar: CuentaPorPagar
    usuario: Usuario
    deuda: Deuda | None
    valor: Decimal
    fecha_creacion: datetime
    tipo_de_descuento: str
    descripcion: str | None
    fecha_actualizacion: datetime | None
