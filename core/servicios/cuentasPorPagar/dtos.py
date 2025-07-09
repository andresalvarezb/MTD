from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario
from core.entidades.cuentaBancaria import CuentaBancaria


@dataclass
class CrearCuentaPorPagarDTO:
    claveCPP: str
    historial_laboral: HistorialLaboralUsuario
    cuenta_bancaria: CuentaBancaria
    fecha_prestacion_servicio: datetime
    fecha_radicacion_contable: datetime
    estado_aprobacion_cuenta_usuario: str
    estado_cuenta_por_pagar: str
    valor_cuenta_cobro: Decimal
    estado_de_pago: str | None
    # total_descuentos: Decimal | None
    # total_a_pagar: Decimal | None
    fecha_actualizacion: datetime | None
    fecha_aprobacion_rut: datetime | None
    fecha_creacion: datetime | None
    fecha_aprobacion_cuenta_usuario: datetime | None
    fecha_programacion_pago: datetime | None
    fecha_reprogramacion: datetime | None
    fecha_pago: datetime | None
    estado_reprogramacion_pago: str | None
    rut: bool | None
    dse: str | None
    causal_rechazo: str | None
    creado_por: str | None
    lider_paciente_asignado: str | None
    eps_paciente_asignado: str | None


@dataclass
class ActualizarCuentaPorPagarDTO:
    historial_laboral: HistorialLaboralUsuario | None
    cuenta_bancaria: CuentaBancaria | None
    estado_aprobacion_cuenta_usuario: str | None
    valor_cuenta_cobro: Decimal | None
    estado_de_pago: str | None
    fecha_aprobacion_rut: datetime | None
    fecha_aprobacion_cuenta_usuario: datetime | None
    fecha_programacion_pago: datetime | None
    fecha_reprogramacion: datetime | None
    fecha_pago: datetime | None
    estado_reprogramacion_pago: str | None
    rut: bool | None
    dse: str | None
    causal_rechazo: str | None
    lider_paciente_asignado: str | None
    eps_paciente_asignado: str | None
