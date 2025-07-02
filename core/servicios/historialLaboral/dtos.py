from datetime import datetime
from dataclasses import dataclass
from core.entidades.cargo import Cargo
from core.entidades.usuario import Usuario
from core.entidades.municipio import Municipio


@dataclass
class ActualizarSeguridadSocialDTO:
    id_usuario: int
    id_cuenta_por_pagar: int
    documento_usuario: str
    tiene_seguridad_social: bool
    fecha_aprobacion_seguridad_social: datetime


@dataclass
class CrearHistorialLaboralUsuarioDTO:
    usuario: Usuario
    contrato: str
    cargo: Cargo
    claveHLU: str
    municipio: Municipio
    seguridad_social: bool | None
    fecha_contratacion: datetime | None
    fecha_fin_contratacion: datetime | None
    fecha_ultima_contratacion: datetime | None
    fecha_aprobacion_seguridad_social: datetime | None


@dataclass
class ActualizarHistorialLaboralUsuarioDTO:
    usuario: Usuario | None
    contrato: str | None
    cargo: Cargo | None
    municipio: Municipio | None
    seguridad_social: bool | None
    fecha_contratacion: datetime | None
    fecha_fin_contratacion: datetime | None
    fecha_ultima_contratacion: datetime | None
    fecha_aprobacion_seguridad_social: datetime | None
