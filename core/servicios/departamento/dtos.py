from dataclasses import dataclass


@dataclass
class CrearDepartamentoDTO:
    nombre: str


@dataclass
class ObtenerDepartamentoDTO:
    nombre: str
