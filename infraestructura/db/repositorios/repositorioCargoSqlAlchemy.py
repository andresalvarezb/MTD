from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.entidades.cargo import Cargo
from infraestructura.db.modelos.cargo import CargoORM
from core.interfaces.repositorioCargo import CrearCargoProtocol, ObtenerCargoPorNombreProtocol


class RepositorioCargoSqlAlchemy(CrearCargoProtocol, ObtenerCargoPorNombreProtocol):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def crear(self, cargo: Cargo) -> Cargo:
        cargo_nuevo = CargoORM(nombre=cargo.nombre)
        self.db.add(cargo_nuevo)
        await self.db.flush()
        await self.db.refresh(cargo_nuevo)
        return Cargo.from_orm(cargo_nuevo)

    async def obtener_por_nombre(self, cargo: str) -> Cargo | None:
        registro_orm = await self.db.execute(select(CargoORM).where(CargoORM.nombre == cargo))
        registro_orm = registro_orm.scalar_one_or_none()
        if registro_orm:
            return Cargo.from_orm(registro_orm)
        else:
            return None
