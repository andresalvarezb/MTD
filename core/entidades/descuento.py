from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime


@dataclass
class Descuento:
    id_cuenta_por_pagar: int
    id_usuario: int
    valor: Decimal
    fecha_creacion: datetime
    tipo_de_descuento: str | None
    id_deuda: int | None = None
    id: int | None = None
    descripcion: str | None = None
    fecha_actualizacion: datetime | None = None

    def __post_init__(self):
        if self.tipo_de_descuento:
            self.tipo_de_descuento = self.tipo_de_descuento.capitalize()

        if self.descripcion:
            self.descripcion = self.descripcion.lower()

    def actualizar_valor(self, nuevo_valor: Decimal):
        if nuevo_valor < 0:
            raise ValueError("El valor del descuento no puede ser negativo.")
        self.valor = nuevo_valor
        self.fecha_actualizacion = datetime.now()

    def actualizar_descripcion(self, nueva_descripcion: str):
        self.descripcion = nueva_descripcion.capitalize()
        self.fecha_actualizacion = datetime.now()

    def actualizar_tipo_de_descuento(self, nuevo_tipo: str):
        self.tipo_de_descuento = nuevo_tipo.capitalize()
        self.fecha_actualizacion = datetime.now()

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            id_cuenta_por_pagar=orm_obj.id_cuenta_por_pagar,
            id_usuario=orm_obj.id_usuario,
            valor=orm_obj.valor,
            fecha_creacion=orm_obj.fecha_creacion,
            tipo_de_descuento=orm_obj.tipo_de_descuento,
            id_deuda=orm_obj.id_deuda,
            descripcion=orm_obj.descripcion,
            fecha_actualizacion=orm_obj.fecha_actualizacion,
        )
