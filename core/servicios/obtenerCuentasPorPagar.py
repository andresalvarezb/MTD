from core.interfaces.repositorioCuentaPorPagar import ObtenerCuentasPorPagarProtocol


class ObtenerCuentasPorPagar:
    def __init__(self, repositorio: ObtenerCuentasPorPagarProtocol):
        self.repositorio = repositorio

    def ejecutar(self):
        return self.repositorio.obtener_cuentas_por_pagar()
