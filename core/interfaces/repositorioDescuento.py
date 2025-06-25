from typing import Protocol, runtime_checkable
from core.entidades.descuento import Descuento


@runtime_checkable
class CrearDescuentoProtocol(Protocol):
    def crear(self, descuento: Descuento) -> Descuento: ...


@runtime_checkable
class ObtenerDescuentosProtocol(Protocol):
    def obtener_descuentos(self) -> list[Descuento]: ...


@runtime_checkable
class ObtenerDescuentoPorIdProtocol(Protocol):
    def obtener_descuento_por_id(self, id_descuento: int) -> Descuento | None: ...


class ObtenerDescuentoProtocol(Protocol):
    def obtener_descuento(self, descuento: Descuento) -> Descuento | None: ...