from core.entidades.cuentaBancaria import CuentaBancaria
from core.interfaces.repositorioCuentaBancaria import CrearCuentaBancariaProtocol,ObtenerCuentaBancariaProtocol
from core.servicios.cuentasBancarias.dtos import CrearCuentaBancariaDTO



class CrearCuentaBancaria:
    def __init__(self, repo_crear: CrearCuentaBancariaProtocol, repo_obtener: ObtenerCuentaBancariaProtocol):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener


    def ejecutar(self, datos: CrearCuentaBancariaDTO) -> CuentaBancaria:
        cuenta_bancaria = CuentaBancaria(
            numero_cuenta=datos.numero_cuenta,
            numero_certificado=datos.numero_certificado,
            estado=datos.estado,
            id_usuario=datos.id_usuario,
            id_banco=datos.id_banco,
            tipo_de_cuenta=datos.tipo_de_cuenta,
            fecha_actualizacion=datos.fecha_actualizacion,
            observaciones=datos.observaciones,
        )

        cuenta_existente = self.repo_obtener.obtener_por_numero(cuenta_bancaria)
        if cuenta_existente:
            return cuenta_existente

        cuenta_bancaria = self.repo_crear.crear(cuenta_bancaria)

        return cuenta_bancaria
