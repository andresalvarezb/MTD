from dataclasses import dataclass
from datetime import datetime


@dataclass
class CrearDepartamentoDTO:
    nombre: str


@dataclass
class CrearMunicipioDTO:
    nombre: str
    id_departamento: int


@dataclass
class CrearCargoDTO:
    nombre: str


@dataclass
class CrearUsuarioDTO:
    documento: str
    nombre: str
    estado: str
    id_municipio: int
    contrato: str
    id_cargo: int
    correo: str
    telefono: str
    seguridad_social: bool
    fecha_aprobacion_seguridad_social: datetime | None
    fecha_ultima_contratacion: datetime | None
