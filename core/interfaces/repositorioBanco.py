from typing import Protocol, runtime_checkable
from core.entidades.banco import Banco


@runtime_checkable
class CrearBancoProtocol(Protocol):
    async def crear(self, banco: Banco) -> Banco: ...


class ObtenerBancoPorNombreProtocol(Protocol):
    async def obtener_por_nombre(self, nombre: str) -> Banco | None: ...
