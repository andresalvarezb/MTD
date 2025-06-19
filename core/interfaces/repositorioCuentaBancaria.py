from typing import Protocol, runtime_checkable
from core.entidades.cuentaBancaria import CuentaBancaria


@runtime_checkable
class RepositorioCuentaBancaria(Protocol):
    def guardar(self, cuenta_bancaria: CuentaBancaria) -> CuentaBancaria: ...
