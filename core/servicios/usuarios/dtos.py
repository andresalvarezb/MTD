from dataclasses import dataclass
from datetime import datetime
from core.entidades.cargo import Cargo
from core.entidades.municipio import Municipio


@dataclass
class CrearCargoDTO:
    nombre: str


@dataclass
class CrearUsuarioDTO:
    documento: str
    nombre: str
    estado: str
    contrato: str
    correo: str
    telefono: str
    cargo: Cargo
    municipio: Municipio
    seguridad_social: bool
    fecha_aprobacion_seguridad_social: datetime | None
    fecha_ultima_contratacion: datetime | None
