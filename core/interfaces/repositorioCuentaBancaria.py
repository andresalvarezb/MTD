from typing import Protocol, runtime_checkable
from core.entidades.cuentaBancaria import CuentaBancaria


class CrearCuentaBancariaProtocol(Protocol):
    def crear(self, cuenta_bancaria: CuentaBancaria) -> CuentaBancaria: ...


class ObtenerCuentaBancariaProtocol(Protocol):
    def obtener_por_numero(self, cuenta_bancaria: CuentaBancaria) -> CuentaBancaria | None: ...


class ObtenerCuentaBancariaPorIdProtocol(Protocol):
    def obtener_por_id(self, id_cuenta_bancaria: int) -> CuentaBancaria | None: ...