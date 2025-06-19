from dataclasses import dataclass


@dataclass
class Banco:
    id: int
    nombre: str
    descripcion: str | None = None

    def _actualizar_nombre_banco(self, nuevo_nombre: str):
        self.nombre = nuevo_nombre.capitalize()

    def _actualizar_descripcion_banco(self, nueva_descripcion: str):
        self.descripcion = nueva_descripcion.capitalize()
