from dataclasses import dataclass
from infraestructura.db.modelos.departamento import DepartamentoORM

@dataclass
class Departamento:
    nombre: str
    id: int | None = None

    def __post_init__(self):
        self.nombre = self.nombre.upper()

    @classmethod
    def from_orm(cls, orm_object: DepartamentoORM) -> "Departamento":
        return cls(
            id=orm_object.id,
            nombre=orm_object.nombre,
        )
