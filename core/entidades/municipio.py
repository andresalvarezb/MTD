from dataclasses import dataclass


@dataclass
class Municipio:
    nombre: str
    id_departamento: int
    id: int | None = None

    def __post_init__(self):
        self.nombre = self.nombre.upper()


@dataclass
class Departamento:
    nombre: str
    id: int | None = None

    def __post_init__(self):
        self.nombre = self.nombre.upper()
