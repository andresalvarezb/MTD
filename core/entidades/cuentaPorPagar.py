from decimal import Decimal
from datetime import datetime
from .descuento import Descuento
from dataclasses import dataclass
from core.entidades.cuentaBancaria import CuentaBancaria
from infraestructura.db.modelos.cuentaPorPagar import CuentaPorPagarORM
from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario


@dataclass
class CuentaPorPagar:

    historial_laboral: HistorialLaboralUsuario
    cuenta_bancaria: CuentaBancaria
    claveCPP: str
    fecha_prestacion_servicio: datetime
    fecha_radicacion_contable: datetime
    estado_aprobacion_cuenta_usuario: str
    estado_cuenta_por_pagar: str
    valor_cuenta_cobro: Decimal
    estado_de_pago: str | None = None
    id: int | None = None
    total_descuentos: Decimal | None = None
    total_a_pagar: Decimal | None = None
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
    eps_paciente_asignado: str | None = None

    def __post_init__(self):
        if self.estado_aprobacion_cuenta_usuario:
            self.estado_aprobacion_cuenta_usuario = self.estado_aprobacion_cuenta_usuario.upper()
        if self.estado_cuenta_por_pagar:
            self.estado_cuenta_por_pagar = self.estado_cuenta_por_pagar.upper()
        if self.estado_de_pago:
            self.estado_de_pago = self.estado_de_pago.upper()
        if self.estado_reprogramacion_pago:
            self.estado_reprogramacion_pago = self.estado_reprogramacion_pago.upper()
        if self.creado_por:
            self.creado_por = self.creado_por.upper()
        if self.lider_paciente_asignado:
            self.lider_paciente_asignado = self.lider_paciente_asignado.upper()
        if self.eps_paciente_asignado:
            self.eps_paciente_asignado = self.eps_paciente_asignado.upper()
        if self.dse:
            self.dse = self.dse.upper()

        # self.total_descuentos = sum((descuento.valor for descuento in descuentos), Decimal(0))

    def calcular_descuentos(self, descuentos: list[Descuento]):
        descuento_total = sum((descuento.valor for descuento in descuentos), Decimal("0.0"))
        self.total_descuentos = descuento_total
        self.total_a_pagar = self.valor_cuenta_cobro - descuento_total

    @classmethod
    def from_orm(cls, orm_obj: CuentaPorPagarORM) -> "CuentaPorPagar":
        return cls(
            historial_laboral=HistorialLaboralUsuario.from_orm(orm_obj.historial_laboral),
            cuenta_bancaria=CuentaBancaria.from_orm(orm_obj.cuenta_bancaria),
            claveCPP=orm_obj.claveCPP,
            fecha_prestacion_servicio=orm_obj.fecha_prestacion_servicio,
            fecha_radicacion_contable=orm_obj.fecha_radicacion_contable,
            estado_aprobacion_cuenta_usuario=orm_obj.estado_aprobacion_cuenta_usuario,
            estado_cuenta_por_pagar=orm_obj.estado_cuenta_por_pagar,
            valor_cuenta_cobro=orm_obj.valor_cuenta_cobro,  # type: ignore
            estado_de_pago=orm_obj.estado_de_pago,
            id=orm_obj.id,
            total_descuentos=orm_obj.total_descuentos,  # type: ignore
            total_a_pagar=orm_obj.total_a_pagar,  # type: ignore
            fecha_actualizacion=orm_obj.fecha_actualizacion,
            fecha_aprobacion_rut=orm_obj.fecha_aprobacion_rut,
            fecha_creacion=orm_obj.fecha_creacion,
            fecha_aprobacion_cuenta_usuario=orm_obj.fecha_aprobacion_cuenta_usuario,
            fecha_programacion_pago=orm_obj.fecha_programacion_pago,
            fecha_reprogramacion=orm_obj.fecha_reprogramacion,
            fecha_pago=orm_obj.fecha_pago,
            estado_reprogramacion_pago=orm_obj.estado_reprogramacion_pago,
            rut=orm_obj.rut,
            dse=orm_obj.dse,
            causal_rechazo=orm_obj.causal_rechazo,
            creado_por=orm_obj.creado_por,
            lider_paciente_asignado=orm_obj.lider_paciente_asignado,
            eps_paciente_asignado=orm_obj.eps_paciente_asignado,
        )
