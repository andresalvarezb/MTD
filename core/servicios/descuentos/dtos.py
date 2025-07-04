from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from core.entidades.deuda import Deuda
from core.entidades.usuario import Usuario
from core.entidades.cuentaPorPagar import CuentaPorPagar


@dataclass
class CrearDescuentoDTO:
    id_cuenta_por_pagar: int
    id_usuario: int
    valor: Decimal
    descripcion: str | None
    id_deuda: int | None = None
    tipo_de_descuento: str | None = None
    fecha_actualizacion: datetime | None = None
    fecha_creacion: datetime | None = None


@dataclass
class FiltrarDescuentosDTO:
    id_cuenta_por_pagar: int | None
    id_usuario: int | None
    id_deuda: int | None = None


@dataclass
class ActualizarDescuentoDTO:
    valor: Decimal | None = None
    tipo_de_descuento: str | None = None
    descripcion: str | None = None
    fecha_actualizacion: datetime | None = None
    fecha_creacion: datetime | None = None
    id_deuda: int | None = None
    id_usuario: int | None = None
    id_cuenta_por_pagar: int | None = None
    id: int | None = None