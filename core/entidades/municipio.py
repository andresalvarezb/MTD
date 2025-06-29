from dataclasses import dataclass
from infraestructura.db.modelos.municipio import DepartamentoORM, MunicipioORM

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

@dataclass
class Municipio:
    nombre: str
    departamento: Departamento
    id: int | None = None

    def __post_init__(self):
        self.nombre = self.nombre.upper()

    @classmethod
    def from_orm(cls, orm_object: MunicipioORM) -> "Municipio":
        return cls(
            id=orm_object.id,
            nombre=orm_object.nombre,
            departamento=Departamento.from_orm(orm_object.departamento),
        )


