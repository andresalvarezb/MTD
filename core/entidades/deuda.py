from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Deuda:
    id_usuario: int
    estado: str
    saldo: Decimal
    valor_total: Decimal
    fecha_creacion: datetime
    fecha_actualizacion: datetime | None
    id_area: int | None = None
    id: int | None = None

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
