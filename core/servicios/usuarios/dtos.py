from dataclasses import dataclass
from datetime import datetime
from core.servicios.municipio.dtos import CrearMunicipioDTO
from core.servicios.cargos.dtos import CrearCargoDTO



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
    documento: str
    nombre: str | None = None
    estado: str | None = None
    contrato: str | None = None
    correo: str | None = None
    telefono: str | None = None
    seguridad_social: bool | None = None
    fecha_aprobacion_seguridad_social: datetime | None = None
    fecha_ultima_contratacion: datetime | None = None
    cargo: CrearCargoDTO | None = None
    municipio: CrearMunicipioDTO | None = None
