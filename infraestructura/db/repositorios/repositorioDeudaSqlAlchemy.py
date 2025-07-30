from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.entidades.deuda import Deuda
from datetime import datetime
from decimal import Decimal
from infraestructura.db.modelos.deuda import DeudaORM
from core.interfaces.repositorioDeuda import (
    CrearDeudaProtocol,
    ObtenerDeudasProtocol,
    ActualizarDeudaProtocol,
    ObtenerDeudaPorIdProtocol,
)


class RepositorioDeudaSqlAlchemy(
    CrearDeudaProtocol, ObtenerDeudasProtocol, ActualizarDeudaProtocol, ObtenerDeudaPorIdProtocol
):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def crear(self, deuda: Deuda) -> Deuda:
        """Implementación para guardar un Deuda en la base de datos"""
        nuevo_deuda = DeudaORM(
            id_usuario=deuda.usuario.id,
            estado=deuda.estado,
            saldo=deuda.saldo,
            valor_total=deuda.valor_total,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
            descripcion=deuda.descripcion,
            id_area=deuda.area.id if deuda.area else None,
        )
        self.db.add(nuevo_deuda)
        await self.db.flush()
        await self.db.refresh(nuevo_deuda)
        return Deuda.from_orm(nuevo_deuda)

    async def obtener_todas(self) -> list[Deuda]:
        deudas = await self.db.execute(select(DeudaORM))
        deudas = deudas.scalars().all()
        return [Deuda.from_orm(deuda) for deuda in deudas]

    async def actualizar(self, deuda: Deuda) -> Deuda:
        """Implementación para actualizar un Deuda en la base de datos"""
        registro_orm = await self.db.execute(select(DeudaORM).where(DeudaORM.id == deuda.id))
        registro_orm = registro_orm.scalar_one_or_none()

        if not registro_orm:
            raise ValueError("Usuario no encontrado")

        if not deuda.usuario.id:
            raise ValueError("Usuario no asociado")

        registro_orm.id_usuario = deuda.usuario.id

        registro_orm.id_area = deuda.area.id if deuda.area else None
        registro_orm.estado = deuda.estado
        registro_orm.saldo = Decimal(deuda.saldo)  # type: ignore
        registro_orm.valor_total = Decimal(deuda.valor_total)  # type: ignore
        registro_orm.fecha_actualizacion = datetime.now()
        registro_orm.descripcion = deuda.descripcion

        # Sincronizar con la sesión (no guarda todavía)
        await self.db.flush()
        return Deuda.from_orm(registro_orm)

    async def obtener_por_id(self, id_deuda: int) -> Deuda | None:
        registro_orm = await self.db.execute(select(DeudaORM).where(DeudaORM.id == id_deuda))
        registro_orm = registro_orm.scalar_one_or_none()
        if registro_orm:
            return Deuda.from_orm(registro_orm)
        return None

    async def eliminar(self, id_deuda: int) -> None:
        registro_orm = await self.db.execute(select(DeudaORM).where(DeudaORM.id == id_deuda))
        registro_orm = registro_orm.scalar_one_or_none()
        if not registro_orm:
            raise ValueError(f"No hay deuda identificada al id {id_deuda}")

        await self.db.delete(registro_orm)
