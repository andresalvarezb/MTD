from core.interfaces.repositorioAreaMTD import CrearAreaMTDProtocol, ObtenerAreaPorNombreProtocol
from core.entidades.areaMtd import AreaMTD


class CrearAreaMTD:
    def __init__(self, repo_crear: CrearAreaMTDProtocol, repo_obtener: ObtenerAreaPorNombreProtocol):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    def ejecutar(self, nombre: str):

        area_mtd = AreaMTD(nombre=nombre)

        # validar existencia
        area_existente = self.repo_obtener.obtener_por_nombre(area_mtd.nombre)
        if area_existente:
            return area_existente

        nueva_area = self.repo_crear.crear(area_mtd)
        return nueva_area
