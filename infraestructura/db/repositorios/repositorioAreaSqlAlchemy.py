from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.entidades.areaMtd import AreaMTD
from infraestructura.db.modelos.areaMTD import AreaMTDORM
from core.interfaces.repositorioAreaMTD import (
    ObtenerAreaPorNombreProtocol,
    CrearAreaMTDProtocol,
    ObtenerAreasProtocol,
    ObtnerAreaPorIdProtocol,
    EliminarAreaMTDProtocol,
)


class RepositorioAreaMTDSqlAlchemy(
    CrearAreaMTDProtocol, ObtenerAreaPorNombreProtocol, ObtenerAreasProtocol, ObtnerAreaPorIdProtocol
):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def crear(self, area: AreaMTD) -> AreaMTD:
        """Implementación para guardar el AreaMTD en la base de datos"""

        nueva_area = AreaMTDORM(nombre=area.nombre)
        self.db.add(nueva_area)
        await self.db.flush()
        await self.db.refresh(nueva_area)
        return AreaMTD.from_orm(nueva_area)

    async def obtener_por_nombre(self, nombre_area: str) -> AreaMTD | None:
        resultado = await self.db.execute(select(AreaMTDORM).where(AreaMTDORM.nombre==nombre_area))
        registro_orm = resultado.scalar_one_or_none()
        if not registro_orm:
            return None
        return AreaMTD.from_orm(registro_orm)

    async def obtener_todos(self) -> list[AreaMTD]:
        resultado = await self.db.execute(select(AreaMTDORM))
        registros_orm = resultado.scalars().all()
        return [AreaMTD.from_orm(registro_orm) for registro_orm in registros_orm]

    async def obtener_por_id(self, id_area: int) -> AreaMTD | None:
        resultado = await self.db.execute(select(AreaMTDORM).where(AreaMTDORM.id==id_area))
        registro_orm = resultado.scalar_one_or_none()
        if not registro_orm:
            return None
        return AreaMTD.from_orm(registro_orm)

    async def eliminar(self, id_area: int) -> None:
        resultado = await self.db.execute(select(AreaMTDORM).where(AreaMTDORM.id==id_area))
        registro_orm = resultado.scalar_one_or_none()
        if not registro_orm:
            raise ValueError(f"Area con ID {id_area} no encontrado.")

        await self.db.delete(registro_orm)
        await self.db.flush()
