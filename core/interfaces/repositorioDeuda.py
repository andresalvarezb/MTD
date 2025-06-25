from core.entidades.deuda import Deuda
from typing import Protocol


class CrearDeudaProtocol(Protocol):
    def crear(self, deuda: Deuda) -> Deuda: ...

class ObtenerDeudasProtocol(Protocol):
    def obtener_todas(self) -> list[Deuda]: ...