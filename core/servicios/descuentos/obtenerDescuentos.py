from core.interfaces.repositorioDescuento import ObtenerDescuentosProtocol
from core.servicios.descuentos.dtos import FiltrarDescuentosDTO


class ObtenerDescuentos:
    def __init__(self, repositorio: ObtenerDescuentosProtocol):
        self.repositorio = repositorio

    def ejecutar(self, filtros: FiltrarDescuentosDTO):
        return self.repositorio.obtener_descuentos(filtros)
