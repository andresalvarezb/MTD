from typing import Protocol, runtime_checkable
from core.entidades.cargo import Cargo


@runtime_checkable
class RepositorioCargo(Protocol):
    def guardar(self, cargo: Cargo) -> Cargo: ...
