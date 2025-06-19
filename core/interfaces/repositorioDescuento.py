from typing import Protocol, runtime_checkable
from core.entidades.descuento import Descuento


@runtime_checkable
class RepositorioDescuento(Protocol):
    def guardar(self, descuento: Descuento) -> Descuento: ...
