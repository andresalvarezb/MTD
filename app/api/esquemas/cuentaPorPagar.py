from pydantic import BaseModel, Field
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
    id: Optional[int] = Field(None, description="ID único de la cuenta por pagar")
    claveCPP: str = Field(
        ...,
        description="Clave única compuesta para la cuenta por pagar. Es la union del mesdeservicio-documento-mesradicacioncontable",
        examples=["20250501110677908520250601"],
    )
    fecha_prestacion_servicio: Optional[datetime] = Field(
        None,
        description="Fecha en la que se prestó el servicio en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_radicacion_contable: Optional[datetime] = Field(
        None,
        description="Fecha de radicación contable en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )

    estado_de_pago: Optional[str] = Field(
        "PENDIENTE", description="Estado actual del pago (Ej: PENDIENTE, PAGADO, REPROGRAMADO, NO APLICA)"
    )
    estado_aprobacion_cuenta_usuario: str = Field(
        ..., description="Estado de aprobación de la cuenta por parte del usuario (Ej: ACEPTADO, RACHAZADO)"
    )
    estado_cuenta_por_pagar: str = Field(..., description="Estado general de la cuenta por pagar (Ej: PROCEDEPARAPAGO, NO PROCEDEPARAPAGO)")

    valor_cuenta_cobro: Decimal = Field(..., description="Valor bruto de la cuenta de cobro", examples=[100_000])
    total_descuentos: Optional[Decimal] = Field(None, description="Suma de todos los descuentos aplicados", examples=[54_200])
    total_a_pagar: Optional[Decimal] = Field(None, description="Valor final a pagar después de aplicar descuentos", examples=[45_800])

    fecha_actualizacion: Optional[datetime] = Field(
        None,
        description="Fecha de la última actualización del registro en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_aprobacion_rut: Optional[datetime] = Field(
        None,
        description="Fecha en que se aprobó el RUT del usuario en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_creacion: Optional[datetime] = Field(
        None,
        description="Fecha de creación del registro en el sistema en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_aprobacion_cuenta_usuario: Optional[datetime] = Field(
        None, description="Fecha de aprobación de la cuenta por el usuario en formato ISO 8601 YYYY-MM-DDTHH:MM:SS"
    )
    fecha_programacion_pago: Optional[datetime] = Field(
        None,
        description="Fecha en que se programó el pago en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_reprogramacion: Optional[datetime] = Field(
        None,
        description="Fecha de reprogramación del pago en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_pago: Optional[datetime] = Field(
        None,
        description="Fecha en que se realizó el pago  en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )

    estado_reprogramacion_pago: Optional[str] = Field(None, description="Estado de la reprogramación del pago (Ej: PENDIENTE, PAGADO, REPROGRAMADO, NO APLICA)")
    rut: Optional[bool] = Field(None, description="Indica si el RUT fue aprobado (True) o no (False)")
    dse: Optional[str] = Field(None, description="Información sobre DSE asociada")
    causal_rechazo: Optional[str] = Field(None, description="Motivo del rechazo si la cuenta fue rechazada")
    creado_por: Optional[str] = Field(None, description="Usuario o sistema que creó el registro")
    lider_paciente_asignado: Optional[str] = Field(None, description="Nombre del líder asignado al paciente")
    eps_paciente_asignado: Optional[str] = Field(None, description="EPS asignada al paciente")
    tipo_de_cuenta: Optional[str] = Field(None, description="Tipo de cuenta bancaria asociada")

    # Relaciones anidadas
    usuario: "Usuario" = Field(..., description="Información del usuario asociado a la cuenta")
    municipio: "Municipio" = Field(..., description="Municipio donde se originó el servicio")
    departamento: "Departamento" = Field(..., description="Departamento asociado al municipio")
    historial_laboral: "HistorialLaboralUsuario" = Field(
        ..., description="Historial laboral relacionado con esta cuenta"
    )
    cuenta_bancaria: "CuentaBancaria" = Field(..., description="Cuenta bancaria donde se realizará el pago")

    model_config = {"from_attributes": True}
