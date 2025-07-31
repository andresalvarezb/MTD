from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.entidades.banco import Banco
from infraestructura.db.modelos.banco import BancoORM
from core.interfaces.repositorioBanco import CrearBancoProtocol, ObtenerBancoPorNombreProtocol


class RepositorioBancoSqlAlchemy(CrearBancoProtocol, ObtenerBancoPorNombreProtocol):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def crear(self, banco: Banco) -> Banco:
        banco_nuevo = BancoORM(nombre=banco.nombre)
        self.db.add(banco_nuevo)
        await self.db.flush()
        await self.db.refresh(banco_nuevo)
        banco.id = banco_nuevo.id
        return banco

    async def obtener_por_nombre(self, nombre: str) -> Banco | None:
        registro_orm = await self.db.execute(select(BancoORM).where(BancoORM.nombre == nombre))
        registro_orm = registro_orm.scalar_one_or_none()
        if registro_orm:
            return Banco.from_orm(registro_orm)
        else:
            return None
