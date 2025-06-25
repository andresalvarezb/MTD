from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from infraestructura.db.modelos.deuda import DeudaORM
from typing import cast




@dataclass
class Deuda:
    id_usuario: int
    estado: str
    saldo: Decimal
    valor_total: Decimal
    fecha_creacion: datetime
    fecha_actualizacion: datetime | None = None
    id_area: int | None = None
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
            id_usuario=orm_obj.id_usuario,
            estado=orm_obj.estado,
            saldo=cast(Decimal, orm_obj.saldo), # el cast es para no generar errores de tipo Decimal =! DECIMAL
            valor_total=cast(Decimal, orm_obj.valor_total),
            fecha_creacion=orm_obj.fecha_creacion,
            fecha_actualizacion=orm_obj.fecha_actualizacion,
            id_area=orm_obj.id_area,
            id=orm_obj.id,
            descripcion=orm_obj.descripcion,
        )