from sqlalchemy.orm import Session
from core.entidades.cargo import Cargo
from infraestructura.db.modelos.cargo import CargoORM
from core.interfaces.repositorioCargo import CrearCargoProtocol, ObtenerCargoProtocol


class RepositorioCargoSqlAlchemy(CrearCargoProtocol, ObtenerCargoProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    # def guardar(self, cargo: Cargo) -> Cargo:
    #     """Implementación para guardar el Cargo en la base de datos"""

    #     # verificar existencia
    #     existe = self.obtener(cargo)
    #     if existe:
    #         cargo.id = existe.id
    #         return cargo

    #     # creacion
    #     nuevo_cargo = CargoORM(nombre=cargo.nombre)
    #     self.db.add(nuevo_cargo)
    #     self.db.flush()
    #     self.db.refresh(nuevo_cargo)

    #     cargo.id = nuevo_cargo.id
    #     return cargo

    def obtener_por_nombre(self, cargo: Cargo) -> Cargo | None:
        registro_orm = self.db.query(CargoORM).filter_by(nombre=cargo.nombre).first()
        if registro_orm:
            return Cargo.from_orm(registro_orm)
        else:
            return None

    def crear(self, cargo: Cargo) -> Cargo:
        cargo_nuevo = CargoORM(nombre=cargo.nombre)
        self.db.add(cargo_nuevo)
        self.db.flush()
        self.db.refresh(cargo_nuevo)
        cargo.id = cargo_nuevo.id
        return cargo