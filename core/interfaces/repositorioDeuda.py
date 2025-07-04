from core.entidades.deuda import Deuda
from typing import Protocol


class CrearDeudaProtocol(Protocol):
    def crear(self, deuda: Deuda) -> Deuda: ...


class ObtenerDeudasProtocol(Protocol):
    def obtener_todas(self) -> list[Deuda]: ...


class ActualizarDeudaProtocol(Protocol):
    def actualizar(self, deuda: Deuda) -> Deuda: ...


class ObtenerDeudaPorIdProtocol(Protocol):
    def obtener_por_id(self, id_deuda: int) -> Deuda | None: ...


class EliminarDeudaProtocol(Protocol):
    def eliminar(self, id_deuda: int) -> None: ...
