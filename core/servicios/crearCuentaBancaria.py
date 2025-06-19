from core.entidades.cuentaBancaria import CuentaBancaria
from core.interfaces.repositorioCuentaBancaria import RepositorioCuentaBancaria


class CrearCuentaBancaria:
    def __init__(self, repositorio: RepositorioCuentaBancaria):
        self.repositorio = repositorio

    def ejecutar(self, datos: dict) -> CuentaBancaria:
        cuenta_bancaria = CuentaBancaria(
            numero_cuenta=datos["numero_cuenta"],
            numero_certificado=datos["numero_certificado"],
            estado=datos["estado"],
            id_usuario=datos["id_usuario"],
            id_banco=datos["id_banco"],
            tipo_de_cuenta=datos["tipo_de_cuenta"],
            fecha_actualizacion=datos["fecha_actualizacion"],
            observaciones=datos["observaciones"],
        )

        cuenta_bancaria = self.repositorio.guardar(cuenta_bancaria)

        return cuenta_bancaria
