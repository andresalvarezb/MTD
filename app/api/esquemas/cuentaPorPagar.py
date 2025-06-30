from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

from .historialLaboralUsuario import HistorialLaboralResponseSchema
from .cuentaBancaria import CuentaBancariaResponseSchema


class CuentaPorPagarResponseSchema(BaseModel):
    id: int = Field(..., description="ID único de la cuenta por pagar")
    claveCPP: str = Field(
        ...,
        description="Clave única compuesta para la cuenta por pagar. Es la union del mesdeservicio-documento-mesradicacioncontable",
        examples=["20250501110677908520250601"],
    )
    fecha_prestacion_servicio: datetime | None = Field(
        None,
        description="Fecha en la que se prestó el servicio en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_radicacion_contable: datetime | None = Field(
        None,
        description="Fecha de radicación contable en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )

    estado_de_pago: str | None = Field(
        "PENDIENTE", description="Estado actual del pago (Ej: PENDIENTE, PAGADO, REPROGRAMADO, NO APLICA)"
    )
    estado_aprobacion_cuenta_usuario: str = Field(
        ..., description="Estado de aprobación de la cuenta por parte del usuario (Ej: ACEPTADO, RACHAZADO)"
    )
    estado_cuenta_por_pagar: str = Field(
        ..., description="Estado general de la cuenta por pagar (Ej: PROCEDEPARAPAGO, NO PROCEDEPARAPAGO)"
    )

    valor_cuenta_cobro: Decimal = Field(..., description="Valor bruto de la cuenta de cobro", examples=[100_000])
    total_descuentos: Decimal = Field(..., description="Suma de todos los descuentos aplicados", examples=[54_200])
    total_a_pagar: Decimal = Field(
        ..., description="Valor final a pagar después de aplicar descuentos", examples=[45_800]
    )

    fecha_actualizacion: datetime | None = Field(
        None,
        description="Fecha de la última actualización del registro en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_aprobacion_rut: datetime | None = Field(
        None,
        description="Fecha en que se aprobó el RUT del usuario en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_creacion: datetime | None = Field(
        None,
        description="Fecha de creación del registro en el sistema en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_aprobacion_cuenta_usuario: datetime | None = Field(
        None, description="Fecha de aprobación de la cuenta por el usuario en formato ISO 8601 YYYY-MM-DDTHH:MM:SS"
    )
    fecha_programacion_pago: datetime | None = Field(
        None,
        description="Fecha en que se programó el pago en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_reprogramacion: datetime | None = Field(
        None,
        description="Fecha de reprogramación del pago en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )
    fecha_pago: datetime | None = Field(
        None,
        description="Fecha en que se realizó el pago  en formato ISO 8601 YYYY-MM-DDTHH:MM:SS",
        examples=["2025-06-26T17:16:00", "2025-06-26"],
    )

    estado_reprogramacion_pago: str | None = Field(
        None, description="Estado de la reprogramación del pago (Ej: PENDIENTE, PAGADO, REPROGRAMADO, NO APLICA)"
    )

    rut: bool | None = Field(None, description="Indica si el RUT fue aprobado (True) o no (False)")
    dse: str | None = Field(None, description="Información sobre DSE asociada")
    causal_rechazo: str | None = Field(None, description="Motivo del rechazo si la cuenta fue rechazada")
    creado_por: str | None = Field(None, description="Usuario o sistema que creó el registro")
    lider_paciente_asignado: str | None = Field(None, description="Nombre del líder asignado al paciente")
    eps_paciente_asignado: str | None = Field(None, description="EPS asignada al paciente")

    # Relaciones anidadas
    historial_laboral: HistorialLaboralResponseSchema = Field(
        ..., description="Historial laboral relacionado con esta cuenta"
    )
    cuenta_bancaria: CuentaBancariaResponseSchema = Field(..., description="Cuenta bancaria donde se realizará el pago")

    model_config = {"from_attributes": True}
