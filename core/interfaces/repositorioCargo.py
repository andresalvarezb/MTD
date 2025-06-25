from typing import Protocol, runtime_checkable
from core.entidades.cargo import Cargo



class CrearCargoProtocol(Protocol):
    def crear(self, cargo: Cargo) -> Cargo: ...


class ObtenerCargoProtocol(Protocol):
    def obtener_por_nombre(self, cargo: Cargo) -> Cargo | None: ...