from dataclasses import dataclass
from core.entidades.departamento import Departamento


@dataclass
class CrearMunicipioDTO:
    nombre: str
    departamento: Departamento


@dataclass
class ObtenerMunicipioDTO:
    nombre: str
