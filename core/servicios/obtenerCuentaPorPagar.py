from core.interfaces.repositorioCuentaPorPagar import ObtenerCuentaPorPagarProtocol


class ObtenerCuentaPorPagar:
    def __init__(self, repositorio: ObtenerCuentaPorPagarProtocol):
        self.repositorio = repositorio
    
    def ejecutar(self, id_cuenta_por_pagar: int):
        return self.repositorio.obtener_cuenta_por_pagar(id_cuenta_por_pagar)