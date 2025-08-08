from core.interfaces.repositorioAreaMTD import CrearAreaMTDProtocol, ObtenerAreaPorNombreProtocol
from core.entidades.areaMtd import AreaMTD


class CrearAreaMTD:
    def __init__(self, repo_crear: CrearAreaMTDProtocol, repo_obtener: ObtenerAreaPorNombreProtocol):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    async def ejecutar(self, nombre: str):
        # validar existencia
        area_existente = await self.repo_obtener.obtener_por_nombre(nombre)
        if area_existente:
            return area_existente

        area_mtd = AreaMTD(nombre)

        nueva_area = await self.repo_crear.crear(area_mtd)
        return nueva_area
