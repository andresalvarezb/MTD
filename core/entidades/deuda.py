from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from infraestructura.db.modelos.deuda import DeudaORM
from typing import cast
from core.entidades.usuario import Usuario
from core.entidades.areaMtd import AreaMTD


@dataclass
class Deuda:
    usuario: Usuario
    estado: str
    saldo: Decimal
    valor_total: Decimal
    fecha_creacion: datetime | None = None
    fecha_actualizacion: datetime | None = None
    area: AreaMTD | None = None
    id: int | None = None
    descripcion: str | None = None

    def actualizar_saldo(self, descuento: Decimal):
        if descuento < 0:
            raise ValueError("El descuento a realizar no puede ser negativo.")
        self.saldo = descuento
        self.fecha_actualizacion = datetime.now()

    def actualizar_valor_total(self, nuevo_valor: Decimal):
        if nuevo_valor < 0:
            raise ValueError("El valor total de la deuda no puede ser negativo.")
        self.valor_total = nuevo_valor
        self.fecha_actualizacion = datetime.now()

    @classmethod
    def from_orm(cls, orm_obj: DeudaORM) -> "Deuda":
        return cls(
            usuario=Usuario.from_orm(orm_obj.usuario),
            estado=orm_obj.estado,
            saldo=cast(Decimal, orm_obj.saldo),  # el cast es para no generar errores de tipo Decimal =! DECIMAL
            valor_total=cast(Decimal, orm_obj.valor_total),
            fecha_creacion=orm_obj.fecha_creacion,
            fecha_actualizacion=orm_obj.fecha_actualizacion,
            area=AreaMTD.from_orm(orm_obj.area),
            id=orm_obj.id,
            descripcion=orm_obj.descripcion,
        )
