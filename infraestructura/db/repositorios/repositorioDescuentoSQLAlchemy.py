from sqlalchemy.orm import Session
from core.entidades.descuento import Descuento
from infraestructura.db.modelos.descuento import DescuentosPorPagarORM
from core.interfaces.repositorioDescuento import (
    CrearDescuentoProtocol,
    ObtenerDescuentosProtocol,
    ObtenerDescuentoPorIdProtocol,
)
from core.servicios.descuentos.dtos import FiltrarDescuentosDTO

class RepositorioDescuentoSqlAlchemy(CrearDescuentoProtocol, ObtenerDescuentosProtocol, ObtenerDescuentoPorIdProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(self, descuento: Descuento) -> Descuento:
        nuevo_descuento = DescuentosPorPagarORM(
            id_cuenta_por_pagar=descuento.id_cuenta_por_pagar,
            id_usuario=descuento.id_usuario,
            id_deuda=descuento.id_deuda,
            valor=descuento.valor,
            fecha_creacion=descuento.fecha_creacion,
            tipo_de_descuento=descuento.tipo_de_descuento,
            descripcion=descuento.descripcion,
            fecha_actualizacion=descuento.fecha_actualizacion,
        )
        self.db.add(nuevo_descuento)
        self.db.flush()
        self.db.refresh(nuevo_descuento)
        return descuento.from_orm(nuevo_descuento)


    def obtener_descuentos(self, filtros: FiltrarDescuentosDTO) -> list[Descuento]:

        query = self.db.query(DescuentosPorPagarORM)

        filtros_query = []

        if filtros.id_cuenta_por_pagar is not None:
            filtros_query.append(DescuentosPorPagarORM.id_cuenta_por_pagar == filtros.id_cuenta_por_pagar)

        if filtros.id_usuario is not None:
            filtros_query.append(DescuentosPorPagarORM.id_usuario == filtros.id_usuario)

        if filtros.id_deuda is not None:
            filtros_query.append(DescuentosPorPagarORM.id_deuda == filtros.id_deuda)

        if filtros_query:
            query = query.filter(*filtros_query)

        registros_orm = query.all()

        if not registros_orm:
            raise Exception("No se encontraron registros")

        return [Descuento.from_orm(orm_obj) for orm_obj in registros_orm]


    def obtener_descuento_por_id(self, id_descuento: int) -> Descuento | None:
        registro_orm = self.db.query(DescuentosPorPagarORM).filter_by(id=id_descuento).first()
        if registro_orm:
            return Descuento.from_orm(registro_orm)
        return None
