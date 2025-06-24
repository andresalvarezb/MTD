from core.interfaces.repositorioDescuento import ObtenerDescuentosProtocol


class ObtenerDescuentos:
    def __init__(self, repositorio: ObtenerDescuentosProtocol):
        self.repositorio = repositorio

    def ejecutar(self):
        return self.repositorio.obtener_descuentos()
