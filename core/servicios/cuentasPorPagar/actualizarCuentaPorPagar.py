from core.interfaces.repositorioCuentaPorPagar import (
    ActualizarCuentaPorPagarProtocol,
    ObtenerCuentaPorPagarPorIdProtocol,
)

from core.servicios.cuentasPorPagar.dtos import ActualizarCuentaPorPagarDTO
from app.api.esquemas.cuentaPorPagar import CuentaPorPagarUpdateSchema
from core.entidades.cuentaPorPagar import CuentaPorPagar


class ActualizarCuentaPorPagar:
    def __init__(
        self, repo_actualizar: ActualizarCuentaPorPagarProtocol, repo_obtener: ObtenerCuentaPorPagarPorIdProtocol
    ):
        self.repo_actualizar = repo_actualizar
        self.repo_obtener = repo_obtener

    def ejecutar(self, info_nueva: ActualizarCuentaPorPagarDTO, info_vieja: CuentaPorPagar):

        for key, value in info_nueva.__dict__.items():
            setattr(info_vieja, key, value)

        cuenta_actualizada = self.repo_actualizar.actualizar(info_vieja)

        return cuenta_actualizada
