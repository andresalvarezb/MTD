from sqlalchemy.orm import Session
from core.entidades.descuento import Descuento
from infraestructura.db.modelos.descuento import DescuentosPorPagarORM
from core.interfaces.repositorioDescuento import (
    CrearDescuentoProtocol,
    ObtenerDescuentosProtocol,
    ObtenerDescuentoPorIdProtocol,
)


class RepositorioDescuentoSqlAlchemy(CrearDescuentoProtocol, ObtenerDescuentosProtocol, ObtenerDescuentoPorIdProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(self, descuento: Descuento) -> Descuento:
        nuevo_descuento = DescuentosPorPagarORM(**descuento.__dict__)
        self.db.add(nuevo_descuento)
        self.db.flush()
        self.db.refresh(nuevo_descuento)
        return descuento.from_orm(nuevo_descuento)

    # def obtener(self, descuento: Descuento):
    #     existe = (
    #         self.db.query(DescuentosPorPagarORM)
    #         .filter_by(
    #             id_cuenta_por_pagar=descuento.cuenta_por_pagar.id,
    #             id_usuario=descuento.usuario.id,
    #             id_deuda=descuento.deuda.id,
    #             tipo_de_descuento=descuento.tipo_de_descuento,
    #         )
    #         .first()
    #     )
    #     if existe:
    #         return existe
    #     else:
    #         return None

    def obtener_descuentos(self) -> list[Descuento]:
        registros_orm = self.db.query(DescuentosPorPagarORM).all()
        return [Descuento.from_orm(orm_obj) for orm_obj in registros_orm]

    def obtener_descuento_por_id(self, id_descuento: int) -> Descuento | None:
        registro_orm = self.db.query(DescuentosPorPagarORM).filter_by(id=id_descuento).first()
        if registro_orm:
            return Descuento.from_orm(registro_orm)
        return None
