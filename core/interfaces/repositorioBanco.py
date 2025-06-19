from typing import Protocol, runtime_checkable
from core.entidades.banco import Banco


@runtime_checkable
class RepositorioBanco(Protocol):
    def guardar(self, banco: Banco) -> Banco: ...
