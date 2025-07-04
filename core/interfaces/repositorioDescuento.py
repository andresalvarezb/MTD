from typing import Protocol, runtime_checkable
from core.entidades.descuento import Descuento
from core.servicios.descuentos.dtos import FiltrarDescuentosDTO


@runtime_checkable
class CrearDescuentoProtocol(Protocol):
    def crear(self, descuento: Descuento) -> Descuento: ...


@runtime_checkable
class ObtenerDescuentosProtocol(Protocol):
    def obtener_descuentos(self, filtros: FiltrarDescuentosDTO) -> list[Descuento]: ...


@runtime_checkable
class ObtenerDescuentoPorIdProtocol(Protocol):
    def obtener_descuento_por_id(self, id_descuento: int) -> Descuento | None: ...


class ObtenerDescuentoProtocol(Protocol):
    def obtener_descuento(self, descuento: Descuento) -> Descuento | None: ...


class ActualizarDescuentoProtocol(Protocol):
    def actualizar(self, descuento: Descuento) -> Descuento: ...


class EliminarDescuentoProtocol(Protocol):
    def eliminar(self, id_descuento: int) -> None: ...
