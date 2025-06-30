from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from core.entidades.deuda import Deuda
from core.entidades.usuario import Usuario
from core.entidades.cuentaPorPagar import CuentaPorPagar



@dataclass
class Descuento:
    cuenta_por_pagar: CuentaPorPagar
    usuario: Usuario
    valor: Decimal
    fecha_creacion: datetime
    tipo_de_descuento: str
    deuda: Deuda | None = None
    id: int | None = None
    descripcion: str | None = None
    fecha_actualizacion: datetime | None = None

    def __post_init__(self):
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
            cuenta_por_pagar=orm_obj.cuenta_por_pagar,
            usuario=orm_obj.usuario,
            valor=orm_obj.valor,
            fecha_creacion=orm_obj.fecha_creacion,
            tipo_de_descuento=orm_obj.tipo_de_descuento,
            deuda=orm_obj.deuda,
            descripcion=orm_obj.descripcion,
            fecha_actualizacion=orm_obj.fecha_actualizacion,
        )
