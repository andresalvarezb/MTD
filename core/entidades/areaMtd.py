from dataclasses import dataclass


@dataclass
class AreaMTD:
    id: int
    nombre: str
    descripcion: str | None = None

    def _actualizar_nombre_area(self, nuevo_nombre: str):
        self.nombre = nuevo_nombre.capitalize()

    def _actualizar_descripcion_area(self, nueva_descripcion: str):
        self.descripcion = nueva_descripcion.capitalize()
