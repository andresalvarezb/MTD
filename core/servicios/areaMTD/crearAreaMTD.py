from core.interfaces.repositorioAreaMTD import CrearAreaMTDProtocol
from core.servicios.areaMTD.obtenerAreasMTD import ObtenerAreasMTD
from core.entidades.areaMtd import AreaMTD


class CrearAreaMTD:
    def __init__(self, repo_crear: CrearAreaMTDProtocol, repo_obtener: ObtenerAreasMTD):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    async def ejecutar(self, nombre: str, id_area: int | None = None):
        # validar existencia
        area_existente = await self.repo_obtener.ejecutar(id_area)
        if area_existente:
            return area_existente

        area_mtd = AreaMTD(nombre)

        nueva_area = await self.repo_crear.crear(area_mtd)
        return nueva_area
