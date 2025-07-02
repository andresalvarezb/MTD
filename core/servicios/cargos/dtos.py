from dataclasses import dataclass


@dataclass
class CrearCargoDTO:
    nombre: str


@dataclass
class ObtenerCargoDTO:
    nombre: str
