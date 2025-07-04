from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class CrearDeudaDTO:
    documento: str
    monto: Decimal
    fecha_creacion: datetime
    area: str | None = None
    descripcion: str | None = None


@dataclass(frozen=True)
class ActualizarDeudaDTO:
    area: str | None = None
    monto: Decimal | None = None
    descripcion: str | None = None
