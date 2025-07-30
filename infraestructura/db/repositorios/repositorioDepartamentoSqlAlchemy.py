from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.entidades.departamento import Departamento
from infraestructura.db.modelos.departamento import DepartamentoORM
from core.interfaces.repositorioDepartamento import (
    CrearDepartamentoProtocol,
    ObtenerDepartamentoPorNombreProtocol,
    ObtenerDepartamentoPorIdProtocol,
)


class RepositorioDepartamentoSqlAlchemy(
    CrearDepartamentoProtocol, ObtenerDepartamentoPorNombreProtocol, ObtenerDepartamentoPorIdProtocol
):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def crear(self, departamento: Departamento) -> Departamento:
        nuevo_departamento = DepartamentoORM(nombre=departamento.nombre)
        self.db.add(nuevo_departamento)
        await self.db.flush()
        await self.db.refresh(nuevo_departamento)
        return Departamento.from_orm(nuevo_departamento)

    async def obtener_por_nombre(self, departamento: Departamento) -> Departamento | None:
        registro_orm = await self.db.execute(select(DepartamentoORM).where(DepartamentoORM.nombre==departamento.nombre))
        registro_orm = registro_orm.scalar_one_or_none()
        if registro_orm:
            return Departamento.from_orm(registro_orm)
        else:
            return None

    async def obtener_por_id(self, id_departamento: int) -> Departamento | None:
        registro_orm = await self.db.execute(select(DepartamentoORM).where(DepartamentoORM.id==id_departamento))
        registro_orm = registro_orm.scalar_one_or_none()
        if registro_orm:
            return Departamento.from_orm(registro_orm)
        else:
            return None
