from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime


@dataclass
class Descuento:
    id_cuenta_por_pagar: int
    id_usuario: int
    valor: Decimal
    fecha_creacion: datetime
    tipo_de_descuento: str
    id_deuda: int | None = None
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
