from dataclasses import dataclass


@dataclass
class AreaMTD:
    nombre: str
    id: int | None = None

    def __post_init__(self):
        self._actualizar_nombre_area(self.nombre)

    def _actualizar_nombre_area(self, nuevo_nombre: str):
        self.nombre = nuevo_nombre.upper()

    @classmethod
    def from_orm(cls, orm_object):
        return cls(id=orm_object.id, nombre=orm_object.nombre)
