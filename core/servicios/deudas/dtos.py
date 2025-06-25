from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class CrearDeudaDTO:
    documento: str
    monto: Decimal
    fecha_creacion: datetime
    area: str
    descripcion: str | None
