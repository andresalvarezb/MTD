from sqlalchemy.orm import Session
from core.entidades.cargo import Cargo
from infraestructura.db.modelos.cargo import CargoORM
from core.interfaces.repositorioCargo import RepositorioCargo


class RepositorioCargoSqlAlchemy(RepositorioCargo):
    def __init__(self, db: Session) -> None:
        self.db = db

    def guardar(self, cargo: Cargo) -> Cargo:
        """Implementación para guardar el Cargo en la base de datos"""

        # verificar existencia
        existe = self.obtener(cargo)
        if existe:
            cargo.id = existe.id
            return cargo

        # creacion
        nuevo_cargo = CargoORM(nombre=cargo.nombre)
        self.db.add(nuevo_cargo)
        self.db.flush()
        self.db.refresh(nuevo_cargo)

        cargo.id = nuevo_cargo.id
        return cargo

    def obtener(self, Cargo: Cargo):
        existe = self.db.query(CargoORM).filter_by(nombre=Cargo.nombre).first()
        if existe:
            return existe
        else:
            return None
