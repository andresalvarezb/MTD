from pydantic import BaseModel


class WrapperRespuesta(BaseModel):
    mensaje: str
    status_code: int
    data: dict | list | str | None

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional, List


class DepartamentoRead(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True


class MunicipioRead(BaseModel):
    id: int
    nombre: str
    departamento: DepartamentoRead

    class Config:
        orm_mode = True


class CargoRead(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True


class BancoRead(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True


class CuentaBancariaRead(BaseModel):
    id: int
    numero_cuenta: str
    numero_certificado: Optional[str]
    estado: str
    tipo_de_cuenta: Optional[str]
    fecha_actualizacion: Optional[datetime]
    observaciones: Optional[str]
    banco: BancoRead

    class Config:
        orm_mode = True


class UsuarioRead(BaseModel):
    id: int
    documento: str
    nombre: str
    correo: str
    telefono: str
    estado: str
    contrato: str
    seguridad_social: bool
    fecha_aprobacion_seguridad_social: Optional[datetime]
    fecha_ultima_contratacion: Optional[datetime]
    municipio: MunicipioRead
    cargo: CargoRead

    class Config:
        orm_mode = True


class HistorialLaboralRead(BaseModel):
    id: int
    contrato: str
    fecha_contratacion: datetime
    fecha_ultima_contratacion: datetime
    seguridad_social: bool
    fecha_aprobacion_seguridad_social: Optional[datetime]
    municipio: MunicipioRead
    cargo: CargoRead
    usuario: UsuarioRead

    class Config:
        orm_mode = True


class DescuentoRead(BaseModel):
    id: int
    tipo_de_descuento: str
    valor: Decimal
    descripcion: Optional[str]
    fecha_creacion: datetime

    class Config:
        orm_mode = True

class CuentaPorPagarRead(BaseModel):
    id: int
    fecha_radicacion_contable: datetime
    fecha_prestacion_servicio: datetime
    fecha_aprobacion_cuenta_usuario: Optional[datetime] = None
    fecha_programacion_pago: Optional[datetime] = None
    fecha_reprogramacion: Optional[datetime] = None
    fecha_pago: Optional[datetime] = None
    fecha_aprobacion_rut: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    fecha_creacion: datetime

    estado_aprobacion_cuenta_usuario: str
    estado_cuenta_por_pagar: str
    estado_de_pago: str
    estado_reprogramacion_pago: Optional[str]
    rut: bool
    dse: Optional[str]
    causal_rechazo: Optional[str]

    lider_paciente_asignado: Optional[str]
    eps_paciente_asignado: Optional[str]
    tipo_de_cuenta: Optional[str]
    creado_por: Optional[str]

    total_descuentos: Decimal
    total_a_pagar: Decimal

    historial_laboral: HistorialLaboralRead
    cuenta_bancaria: CuentaBancariaRead
    descuentos: List[DescuentoRead]

    class Config:
        orm_mode = True
