from dataclasses import dataclass
from datetime import datetime
from core.entidades.cargo import Cargo
from core.entidades.municipio import Municipio

@dataclass
class CrearCargoDTO:
    nombre: str

@dataclass
class CrearDepartamentoDTO:
    nombre: str

@dataclass
class CrearMunicipioDTO:
    nombre: str
    departamento: CrearDepartamentoDTO


@dataclass
class CrearUsuarioDTO:
    documento: str
    nombre: str
    estado: str
    contrato: str
    cargo: CrearCargoDTO
    municipio: CrearMunicipioDTO
    correo: str | None
    telefono: str | None
    seguridad_social: bool | None
    fecha_aprobacion_seguridad_social: datetime | None
    fecha_ultima_contratacion: datetime | None


@dataclass
class ActualizarUsuarioDTO:
    documento: str | None
    nombre: str | None
    estado: str | None
    contrato: str | None
    correo: str | None
    telefono: str | None
    seguridad_social: bool | None
    fecha_aprobacion_seguridad_social: datetime | None
    cargo: Cargo | None
    municipio: Municipio | None
