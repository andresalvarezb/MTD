from datetime import datetime
from dataclasses import dataclass


@dataclass
class ActualizarSeguridadSocialDTO:
    id_usuario: int
    id_cuenta_por_pagar: int
    documento_usuario: str
    tiene_seguridad_social: bool
    fecha_aprobacion_seguridad_social: datetime


@dataclass
class CrearHistorialLaboralUsuarioDTO:
    id_municipio: int
    contrato: str
    id_cargo: int
    claveHLU: str
    id_usuario: int
    fecha_contratacion: datetime | None
    seguridad_social: bool | None
    fecha_aprobacion_seguridad_social: datetime | None
    fecha_ultima_contratacion: datetime | None
    fecha_fin_contratacion: datetime | None
