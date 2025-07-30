from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import select
from core.entidades.descuento import Descuento
from infraestructura.db.modelos.descuento import DescuentosPorPagarORM
from core.interfaces.repositorioDescuento import (
    CrearDescuentoProtocol,
    ObtenerDescuentosProtocol,
    ObtenerDescuentoPorIdProtocol,
    ActualizarDescuentoProtocol,
)
from core.servicios.descuentos.dtos import FiltrarDescuentosDTO


class RepositorioDescuentoSqlAlchemy(
    CrearDescuentoProtocol, ObtenerDescuentosProtocol, ObtenerDescuentoPorIdProtocol, ActualizarDescuentoProtocol
):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def crear(self, descuento: Descuento) -> Descuento:
        nuevo_descuento = DescuentosPorPagarORM(
            id_cuenta_por_pagar=descuento.id_cuenta_por_pagar,
            id_usuario=descuento.id_usuario,
            id_deuda=descuento.id_deuda,
            valor=descuento.valor,
            fecha_creacion=datetime.now(),
            tipo_de_descuento=descuento.tipo_de_descuento,
            descripcion=descuento.descripcion,
            fecha_actualizacion=datetime.now(),
        )
        self.db.add(nuevo_descuento)
        await self.db.flush()
        await self.db.refresh(nuevo_descuento)
        return descuento.from_orm(nuevo_descuento)

    async def obtener_descuentos(self, filtros: FiltrarDescuentosDTO) -> list[Descuento]:


        filtros_execute = []

        if filtros.id_cuenta_por_pagar is not None:
            filtros_execute.append(DescuentosPorPagarORM.id_cuenta_por_pagar == filtros.id_cuenta_por_pagar)

        if filtros.id_usuario is not None:
            filtros_execute.append(DescuentosPorPagarORM.id_usuario == filtros.id_usuario)

        if filtros.id_deuda is not None:
            filtros_execute.append(DescuentosPorPagarORM.id_deuda == filtros.id_deuda)

        execute = select(DescuentosPorPagarORM)
        if filtros_execute:
            execute = execute.where(*filtros_execute)

        registros_orm = await self.db.execute(execute)
        registros_orm = registros_orm.scalars().all()

        if not registros_orm:
            raise Exception("No se encontraron registros")

        return [Descuento.from_orm(orm_obj) for orm_obj in registros_orm]

    async def obtener_descuento_por_id(self, id_descuento: int) -> Descuento | None:
        registro_orm = await self.db.execute(select(DescuentosPorPagarORM).filter_by(id=id_descuento))
        registro_orm = registro_orm.scalar_one_or_none()
        if registro_orm:
            return Descuento.from_orm(registro_orm)
        return None

    async def actualizar(self, descuento: Descuento) -> Descuento:
        registro_orm = await self.db.execute(select(DescuentosPorPagarORM).filter_by(id=descuento.id))
        registro_orm = registro_orm.scalar_one_or_none()
        if not registro_orm:
            raise ValueError(f"Descuento con ID {descuento.id} no encontrado.")

        registro_orm.valor = descuento.valor  # type: ignore
        registro_orm.fecha_actualizacion = datetime.now()

        if descuento.tipo_de_descuento:
            registro_orm.tipo_de_descuento = descuento.tipo_de_descuento

        if descuento.descripcion:
            registro_orm.descripcion = descuento.descripcion

        await self.db.flush()
        return descuento.from_orm(registro_orm)

    async def eliminar(self, id_descuento: int) -> None:
        registro_orm = await self.db.execute(select(DescuentosPorPagarORM).filter_by(id=id_descuento))
        registro_orm = registro_orm.scalar_one_or_none()
        if not registro_orm:
            raise ValueError(f"Descuento con ID {id_descuento} no encontrado.")

        await self.db.delete(registro_orm)
        await self.db.flush()
        return None
