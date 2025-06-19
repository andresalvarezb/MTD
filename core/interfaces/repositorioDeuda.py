from core.entidades.deuda import Deuda
from typing import Protocol, runtime_checkable


@runtime_checkable
class RepositorioDeuda(Protocol):
    def guardar(self, deuda: Deuda) -> Deuda: ...
