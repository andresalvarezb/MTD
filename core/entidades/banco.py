from dataclasses import dataclass
from infraestructura.db.modelos.banco import BancoORM


@dataclass
class Banco:
    nombre: str
    id: int | None = None

    def _actualizar_nombre_banco(self, nuevo_nombre: str):
        self.nombre = nuevo_nombre.capitalize()

    def _actualizar_descripcion_banco(self, nueva_descripcion: str):
        self.descripcion = nueva_descripcion.capitalize()

    @classmethod
    def from_orm(cls, orm_obj: BancoORM) -> "Banco":
        return cls(
            nombre=orm_obj.nombre,
            id=orm_obj.id
        )