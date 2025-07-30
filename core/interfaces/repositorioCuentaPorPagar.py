from typing import Protocol
from core.entidades.cuentaPorPagar import CuentaPorPagar


class CrearCuentaPorPagarProtocol(Protocol):
    async def crear(self, cuenta_por_pagar: CuentaPorPagar) -> CuentaPorPagar: ...


class ObtenerCuentasPorPagarProtocol(Protocol):
    async def obtener_cuentas_por_pagar(self) -> list[CuentaPorPagar]: ...


class ObtenerCuentaPorPagarProtocol(Protocol):
    async def obtener_cuenta_por_pagar(self, id_cuenta_por_pagar: int) -> CuentaPorPagar: ...


class ObtenerCuentaPorPagarPorClaveProtocol(Protocol):
    async def obtener_por_clave(self, clave: str) -> CuentaPorPagar | None: ...


class ObtenerCuentaPorPagarPorIdProtocol(Protocol):
    async def obtener_por_id(self, id_cuenta_por_pagar: int) -> CuentaPorPagar | None: ...


class ActualizarCuentaPorPagarProtocol(Protocol):
    async def actualizar(self, cuenta_por_pagar: CuentaPorPagar) -> CuentaPorPagar: ...
