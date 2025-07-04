from sqlalchemy.orm import Session
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
    def __init__(self, db: Session):
        self.db = db

    def crear(self, deuda: Deuda) -> Deuda:
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
        self.db.flush()
        self.db.refresh(nuevo_deuda)
        return Deuda.from_orm(nuevo_deuda)

    def obtener_todas(self) -> list[Deuda]:
        deudas = self.db.query(DeudaORM).all()
        return [Deuda.from_orm(deuda) for deuda in deudas]

    def actualizar(self, deuda: Deuda) -> Deuda:
        """Implementación para actualizar un Deuda en la base de datos"""
        registro_orm = self.db.query(DeudaORM).filter_by(id=deuda.id).first()

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
        self.db.flush()
        return Deuda.from_orm(registro_orm)

    def obtener_por_id(self, id_deuda: int) -> Deuda | None:
        registro_orm = self.db.query(DeudaORM).filter_by(id=id_deuda).first()
        if registro_orm:
            return Deuda.from_orm(registro_orm)
        return None

    def eliminar(self, id_deuda: int) -> None:
        registro_orm = self.db.query(DeudaORM).filter_by(id=id_deuda).first()
        if registro_orm:
            raise ValueError(f"No hay deuda identificada al id {id_deuda}")

        self.db.delete(registro_orm)
        return None
