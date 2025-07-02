from core.servicios.cuentasBancarias.dtos import ActualizarCuentaBancariaDTO
from core.interfaces.repositorioCuentaBancaria import (
    ActualizarCuentaBancariaProtocol,
    ObtenerCuentaBancariaPorIdProtocol,
)
from core.entidades.cuentaBancaria import CuentaBancaria
from app.api.esquemas.cuentaBancaria import CuentaBancariaUpdateSchema
from core.entidades.cuentaBancaria import CuentaBancaria


class ActualizarCuentaBancaria:
    def __init__(
        self, repo_obtener: ObtenerCuentaBancariaPorIdProtocol, repo_actualizar: ActualizarCuentaBancariaProtocol
    ):
        self.repo_obtener = repo_obtener
        self.repo_actualizar = repo_actualizar

    def ejecutar(self, info_nueva: ActualizarCuentaBancariaDTO, info_vieja: CuentaBancaria):

        print(info_nueva)
        print(info_vieja)

        for key, value in info_nueva.__dict__.items():
            setattr(info_vieja, key, value)

        cuenta_actualizada = self.repo_actualizar.actualizar(info_vieja)

        return cuenta_actualizada
