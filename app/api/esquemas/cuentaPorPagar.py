from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
# from .historialLaboralUsuario import HistorialLaboralResponseSchema
# from .cuentaBancaria import CuentaBancariaResponseSchema
from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario
from core.entidades.cuentaBancaria import CuentaBancaria
from core.entidades.usuario import Usuario
from core.entidades.municipio import Municipio, Departamento







class CuentaPorPagarResponseSchema(BaseModel):
    id: int | None
    id_historial_laboral: int
    id_cuenta_bancaria: int
    claveCPP: str
    fecha_prestacion_servicio: datetime | None
    fecha_radicacion_contable: datetime | None
    estado_de_pago: str | None
    estado_aprobacion_cuenta_usuario: str
    estado_cuenta_por_pagar: str
    valor_cuenta_cobro: Decimal
    total_descuentos: Decimal | None
    total_a_pagar: Decimal | None
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
    tipo_de_cuenta: str | None

    model_config = {"from_attributes": True}

class CuentaPorPagarCompletoResponseSchema(BaseModel):
    id: int | None
    claveCPP: str
    fecha_prestacion_servicio: datetime | None
    fecha_radicacion_contable: datetime | None
    estado_de_pago: str | None
    estado_aprobacion_cuenta_usuario: str
    estado_cuenta_por_pagar: str
    valor_cuenta_cobro: Decimal
    total_descuentos: Decimal | None
    total_a_pagar: Decimal | None
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
    tipo_de_cuenta: str | None
    usuario: Usuario
    municipio: Municipio
    departamento: Departamento
    historial_laboral: HistorialLaboralUsuario
    cuenta_bancaria: CuentaBancaria

    model_config = {"from_attributes": True}
