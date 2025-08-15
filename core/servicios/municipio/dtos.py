from dataclasses import dataclass

from core.servicios.departamento.dtos import CrearDepartamentoDTO


@dataclass
class CrearMunicipioDTO:
    nombre: str
    departamento: CrearDepartamentoDTO


@dataclass
class ObtenerMunicipioDTO:
    nombre: str
