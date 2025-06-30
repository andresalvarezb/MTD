from sqlalchemy.orm import Session
from core.entidades.cargo import Cargo
from infraestructura.db.modelos.cargo import CargoORM
from core.interfaces.repositorioCargo import CrearCargoProtocol, ObtenerCargoPorNombreProtocol


class RepositorioCargoSqlAlchemy(CrearCargoProtocol, ObtenerCargoPorNombreProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(self, cargo: Cargo) -> Cargo:
        cargo_nuevo = CargoORM(nombre=cargo.nombre)
        self.db.add(cargo_nuevo)
        self.db.flush()
        self.db.refresh(cargo_nuevo)
        return cargo.from_orm(cargo_nuevo)

    def obtener_por_nombre(self, cargo: Cargo) -> Cargo | None:
        registro_orm = self.db.query(CargoORM).filter_by(nombre=cargo.nombre).first()
        if registro_orm:
            return Cargo.from_orm(registro_orm)
        else:
            return None
