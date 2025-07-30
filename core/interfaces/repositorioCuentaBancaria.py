from typing import Protocol, runtime_checkable
from core.entidades.cuentaBancaria import CuentaBancaria


class CrearCuentaBancariaProtocol(Protocol):
    async def crear(self, cuenta_bancaria: CuentaBancaria) -> CuentaBancaria: ...


class ObtenerCuentaBancariaProtocol(Protocol):
    async def obtener_por_numero(self, cuenta_bancaria: CuentaBancaria) -> CuentaBancaria | None: ...


class ObtenerCuentaBancariaPorIdProtocol(Protocol):
    async def obtener_por_id(self, id_cuenta_bancaria: int) -> CuentaBancaria | None: ...


class ActualizarCuentaBancariaProtocol(Protocol):
    async def actualizar(self, cuenta_bancaria: CuentaBancaria) -> CuentaBancaria: ...
