from sqlalchemy.orm import Session
from core.entidades.cuentaPorPagar import CuentaPorPagar
from infraestructura.db.modelos.cuentaPorPagar import CuentaPorPagarORM
from core.interfaces.repositorioCuentaPorPagar import (
    CrearCuentaPorPagarProtocol,
    ObtenerCuentaPorPagarProtocol,
    ObtenerCuentasPorPagarProtocol,
    ObtenerCuentaPorPagarPorClaveProtocol,
)
from fastapi import HTTPException


class RepositorioCuentaPorPagarSqlAlchemy(
    CrearCuentaPorPagarProtocol,
    ObtenerCuentaPorPagarProtocol,
    ObtenerCuentasPorPagarProtocol,
    ObtenerCuentaPorPagarPorClaveProtocol,
):
    def __init__(self, db: Session):
        self.db = db

    # def guardar(self, cuenta_por_pagar: CuentaPorPagar) -> CuentaPorPagar:
    #     """Implementación para guardar un CuentaPorPagar en la base de datos"""

    #     # verificar existencia
    #     existe = self.obtener(cuenta_por_pagar)
    #     if existe:
    #         cuenta_por_pagar.id = existe.id
    #         return cuenta_por_pagar

    #     # creacion
    #     nuevo_cuenta_por_pagar = CuentaPorPagarORM(**cuenta_por_pagar.__dict__)
    #     self.db.add(nuevo_cuenta_por_pagar)
    #     self.db.flush()
    #     self.db.refresh(nuevo_cuenta_por_pagar)

    #     cuenta_por_pagar.id = nuevo_cuenta_por_pagar.id
    #     return cuenta_por_pagar
    def crear(self, cuenta_por_pagar: CuentaPorPagar) -> CuentaPorPagar:
        cuenta_nueva = CuentaPorPagarORM(**cuenta_por_pagar.__dict__)
        self.db.add(cuenta_nueva)
        self.db.commit()
        self.db.refresh(cuenta_nueva)
        cuenta_por_pagar.id = cuenta_nueva.id
        return cuenta_por_pagar

    def obtener(self, cuenta_por_pagar: CuentaPorPagar):
        existe = self.db.query(CuentaPorPagarORM).filter_by(claveCPP=cuenta_por_pagar.claveCPP).first()
        if existe:
            return existe
        else:
            return None

    def actualizar(self, cuenta_por_pagar: CuentaPorPagar, dataToUpdate: dict):
        cuenta_por_pagar_db = self.db.query(CuentaPorPagarORM).filter_by(id=cuenta_por_pagar.id).first()

        if cuenta_por_pagar_db:
            for attr, value in dataToUpdate.items():
                setattr(cuenta_por_pagar_db, attr, value)

    def obtener_cuentas_por_pagar(self) -> list[CuentaPorPagar]:
        registros_orm = self.db.query(CuentaPorPagarORM).all()
        return [CuentaPorPagar.from_orm(orm_obj) for orm_obj in registros_orm]

    def obtener_cuenta_por_pagar(self, id_cuenta_por_pagar: int) -> CuentaPorPagar:
        registro = self.db.query(CuentaPorPagarORM).filter_by(id=id_cuenta_por_pagar).first()
        if not registro:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return CuentaPorPagar.from_orm(registro)

    def obtener_por_clave(self, cuenta_por_pagar: CuentaPorPagar) -> CuentaPorPagar | None:
        registro = self.db.query(CuentaPorPagarORM).filter_by(claveCPP=cuenta_por_pagar.claveCPP).first()
        if not registro:
            return None
        return CuentaPorPagar.from_orm(registro)
