from sqlalchemy.orm import Session
from core.entidades.descuento import Descuento
from infraestructura.db.modelos.descuento import DescuentosPorPagarORM
from core.interfaces.repositorioDescuento import (
    CrearDescuentoProtocol,
    ObtenerDescuentosProtocol,
    ObtenerDescuentoProtocol,
)


class RepositorioDescuentoSqlAlchemy(CrearDescuentoProtocol, ObtenerDescuentosProtocol, ObtenerDescuentoProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    # def guardar(self, descuento: Descuento) -> Descuento:
    #     """Implementación para guardar el descuento en la base de datos"""

    #     # verificar existencia
    #     existe = self.obtener(descuento)
    #     if existe:
    #         descuento.id = existe.id
    #         return descuento

    #     # creacion
    #     nuevo_descuento = DescuentosPorPagarORM(**descuento.__dict__)
    #     self.db.add(nuevo_descuento)
    #     self.db.flush()
    #     self.db.refresh(nuevo_descuento)

    #     descuento.id = nuevo_descuento.id
    #     return descuento

    def crear(self, descuento: Descuento) -> Descuento:
        nuevo_descuento = DescuentosPorPagarORM(**descuento.__dict__)
        self.db.add(nuevo_descuento)
        self.db.flush()
        self.db.refresh(nuevo_descuento)

        descuento.id = nuevo_descuento.id
        return descuento

    def obtener(self, descuento: Descuento):
        existe = (
            self.db.query(DescuentosPorPagarORM)
            .filter_by(
                id_cuenta_por_pagar=descuento.id_cuenta_por_pagar,
                id_usuario=descuento.id_usuario,
                tipo_de_descuento=descuento.tipo_de_descuento,
            )
            .first()
        )
        if existe:
            return existe
        else:
            return None

    def obtener_descuentos(self) -> list[Descuento]:
        registros_orm = self.db.query(DescuentosPorPagarORM).all()
        return [Descuento.from_orm(orm_obj) for orm_obj in registros_orm]

    def obtener_descuento(self, descuento: Descuento) -> Descuento | None:
        registro_orm = (
            self.db.query(DescuentosPorPagarORM)
            .filter_by(
                id_usuario=descuento.id_usuario,
                id_cuenta_por_pagar=descuento.id_cuenta_por_pagar,
                id_deuda=descuento.id_deuda,
                tipo_de_descuento=descuento.tipo_de_descuento,
            )
            .first()
        )
        if registro_orm:
            return Descuento.from_orm(registro_orm)
        return None
