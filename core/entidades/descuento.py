from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime


@dataclass
class Descuento:
    id: int
    id_cuenta_por_pagar: int
    id_usuario: int
    id_deuda: int
    valor: Decimal
    fecha_creacion: datetime
    descripcion: str | None = None
    tipo_de_descuento: str | None = None
    fecha_actualizacion: datetime | None = None

    def actualizar_valor(self, nuevo_valor: Decimal):
        if nuevo_valor < 0:
            raise ValueError("El valor del descuento no puede ser negativo.")
        self.valor = nuevo_valor
        self.fecha_actualizacion = datetime.now()

    def actualizar_descripcion(self, nueva_descripcion: str):
        self.descripcion = nueva_descripcion.capitalize()
        self.fecha_actualizacion = datetime.now()
