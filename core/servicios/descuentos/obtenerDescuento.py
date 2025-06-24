from core.interfaces.repositorioDescuento import ObtenerDescuentoProtocol


class ObtenerDescuento:
    def __init__(self, repositorio: ObtenerDescuentoProtocol):
        self.repositorio = repositorio

    def ejecutar(self, id_descuento: int):
        return self.repositorio.obtener_descuento(id_descuento)
