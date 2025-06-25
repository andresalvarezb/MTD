from typing import Protocol, runtime_checkable
from core.entidades.banco import Banco


@runtime_checkable
class CrearBancoProtocol(Protocol):
    def crear(self, banco: Banco) -> Banco: ...


class ObtenerBancoPorNombreProtocol(Protocol):
    def obtener_por_nombre(self, nombre: str) -> Banco | None: ...