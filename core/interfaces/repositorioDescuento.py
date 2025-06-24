from typing import Protocol, runtime_checkable
from core.entidades.descuento import Descuento


@runtime_checkable
class CrearDescuentoProtocol(Protocol):
    def guardar(self, descuento: Descuento) -> Descuento: ...


@runtime_checkable
class ObtenerDescuentosProtocol(Protocol):
    def obtener_descuentos(self) -> list[Descuento]: ...


@runtime_checkable
class ObtenerDescuentoProtocol(Protocol):
    def obtener_descuento(self, id_descuento: int) -> Descuento: ...
