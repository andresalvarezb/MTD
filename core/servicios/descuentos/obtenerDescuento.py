from core.interfaces.repositorioDescuento import ObtenerDescuentoPorIdProtocol


class ObtenerDescuento:
    def __init__(self, repositorio: ObtenerDescuentoPorIdProtocol):
        self.repositorio = repositorio

    def ejecutar(self, id_descuento: int):
        return self.repositorio.obtener_descuento_por_id(id_descuento)
