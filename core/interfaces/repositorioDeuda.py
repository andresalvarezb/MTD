from core.entidades.deuda import Deuda
from typing import Protocol


class CrearDeudaProtocol(Protocol):
    async def crear(self, deuda: Deuda) -> Deuda: ...


class ObtenerDeudasProtocol(Protocol):
    async def obtener_todas(self) -> list[Deuda]: ...


class ActualizarDeudaProtocol(Protocol):
    async def actualizar(self, deuda: Deuda) -> Deuda: ...


class ObtenerDeudaPorIdProtocol(Protocol):
    async def obtener_por_id(self, id_deuda: int) -> Deuda | None: ...


class EliminarDeudaProtocol(Protocol):
    async def eliminar(self, id_deuda: int) -> None: ...
