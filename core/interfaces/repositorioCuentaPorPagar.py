from typing import Protocol
from core.entidades.cuentaPorPagar import CuentaPorPagar


class RepositorioCuentaPorPagar(Protocol):
    def guardar(self, cuenta_por_pagar: CuentaPorPagar) -> CuentaPorPagar: ...
