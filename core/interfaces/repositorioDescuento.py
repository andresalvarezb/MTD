from typing import Protocol, runtime_checkable
from core.entidades.descuento import Descuento
from core.servicios.descuentos.dtos import FiltrarDescuentosDTO


@runtime_checkable
class CrearDescuentoProtocol(Protocol):
    async def crear(self, descuento: Descuento) -> Descuento: ...


@runtime_checkable
class ObtenerDescuentosProtocol(Protocol):
    async def obtener_descuentos(self, filtros: FiltrarDescuentosDTO) -> list[Descuento]: ...


@runtime_checkable
class ObtenerDescuentoPorIdProtocol(Protocol):
    async def obtener_descuento_por_id(self, id_descuento: int) -> Descuento | None: ...


class ObtenerDescuentoProtocol(Protocol):
    async def obtener_descuento(self, descuento: Descuento) -> Descuento | None: ...


class ActualizarDescuentoProtocol(Protocol):
    async def actualizar(self, descuento: Descuento) -> Descuento: ...


class EliminarDescuentoProtocol(Protocol):
    async def eliminar(self, id_descuento: int) -> None: ...
