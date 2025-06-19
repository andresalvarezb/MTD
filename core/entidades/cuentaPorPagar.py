from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from .descuento import Descuento


@dataclass
class CuentaPorPagar:
    id: int
    id_historial_laboral: int

    fecha_prestacion_servicio: datetime
    fecha_radicacion_contable: datetime
    estado_pago: str
    estado_aprobacion_cuenta_usuario: str
    estado_cuenta_por_pagar: str
    valor_cuenta_cobro: Decimal
    descuentos: list[Descuento] = field(default_factory=list)
    total_pago: Decimal | None = None
    fecha_actualizacion: datetime | None = None
    fecha_aprobacion_rut: datetime | None = None
    fecha_creacion: datetime | None = None
    fecha_aprobacion_cuenta_usuario: datetime | None = None
    fecha_programacion_pago: datetime | None = None
    fecha_reprogramacion: datetime | None = None
    fecha_pago: datetime | None = None
    estado_reprogramacion_pago: str | None = None
    rut: bool | None = None
    dse: str | None = None
    causal_rechazo: str | None = None
    creado_por: str | None = None
    lider_paciente_asignado: str | None = None
    id_eps_paciente_asignado: int | None = None

    def calcular_descuentos(self) -> Decimal:
        return sum((descuento.valor for descuento in self.descuentos), Decimal(0))

    def calcular_total_pago(self):
        return self.valor_cuenta_cobro - self.calcular_descuentos()

    def actualizar_total_pago(self):
        self.total_pago = self.calcular_total_pago()