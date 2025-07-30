from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.entidades.municipio import Municipio
from infraestructura.db.modelos.municipio import MunicipioORM
from core.interfaces.repositorioMunicipio import (
    CrearMunicipioProtocol,
    ObtenerMunicipioPorNombreProtocol,
    ObtenerMunicipioPorIdProtocol,
)


class RepositorioMunicipioSqlAlchemy(
    CrearMunicipioProtocol, ObtenerMunicipioPorNombreProtocol, ObtenerMunicipioPorIdProtocol
):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crear(self, municipio: Municipio) -> Municipio:
        if not municipio.departamento:
            raise ValueError("El municipio debe estar asociado a un departamento")

        nuevo_municipio = MunicipioORM(nombre=municipio.nombre, id_departamento=municipio.departamento.id)
        self.db.add(nuevo_municipio)
        await self.db.flush()
        await self.db.refresh(nuevo_municipio)
        return Municipio.from_orm(nuevo_municipio)

    async def obtener_por_nombre(self, municipio: Municipio) -> Municipio | None:
        registro_orm = await self.db.execute(select(MunicipioORM).where(MunicipioORM.nombre==municipio.nombre))
        registro_orm = registro_orm.scalar_one_or_none()
        if registro_orm:
            return Municipio.from_orm(registro_orm)
        else:
            return None

    async def obtener_por_id(self, id_municipio: int) -> Municipio | None:
        registro_orm = await self.db.execute(select(MunicipioORM).where(MunicipioORM.id==id_municipio))
        registro_orm = registro_orm.scalar_one_or_none()
        if registro_orm:
            return Municipio.from_orm(registro_orm)
        else:
            return None
