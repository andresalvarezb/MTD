from dataclasses import dataclass


@dataclass
class AreaMTD:
    id: int
    nombre: str

    def _actualizar_nombre_area(self, nuevo_nombre: str):
        self.nombre = nuevo_nombre.capitalize()

    @classmethod
    def from_orm(cls, orm_object):
        return cls(id=orm_object.id, nombre=orm_object.nombre)
