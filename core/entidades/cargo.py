from dataclasses import dataclass


@dataclass
class Cargo:
    nombre: str
    id: int | None = None

    def __post_init__(self):
        self.nombre = self.nombre.upper()

    def _actualizar_nombre_cargo(self, nuevo_nombre: str):
        self.nombre = nuevo_nombre.capitalize()
