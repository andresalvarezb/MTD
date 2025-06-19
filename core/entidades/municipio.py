from dataclasses import dataclass


@dataclass
class Municipio:
    id: int
    nombre: str
    id_departamento: int


@dataclass
class Departamento:
    id: int
    nombre: str