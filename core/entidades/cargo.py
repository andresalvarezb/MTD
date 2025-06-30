from dataclasses import dataclass
from infraestructura.db.modelos.cargo import CargoORM


@dataclass
class Cargo:
    nombre: str
    id: int | None = None

    def __post_init__(self):
        self.nombre = self.nombre.upper()

    def _actualizar_nombre_cargo(self, nuevo_nombre: str):
        self.nombre = nuevo_nombre.upper()

    @classmethod
    def from_orm(cls, orm_object: CargoORM) -> "Cargo":
        return cls(
            id=orm_object.id,
            nombre=orm_object.nombre,
        )
