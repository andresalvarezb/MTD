from core.interfaces.repositorioAreaMTD import ObtnerAreaPorIdProtocol, ObtenerAreasProtocol
from core.servicios.utilities.exepciones import AreaNoExisteError
from core.entidades.areaMtd import AreaMTD


class ObtenerAreasMTD:
    def __init__(self, repo_area: ObtnerAreaPorIdProtocol, repo_areas: ObtenerAreasProtocol):
        self.repo_area = repo_area
        self.repo_areas = repo_areas

    async def ejecutar(self, id_area: int | None = None) -> list[AreaMTD]:

        if id_area:
            area = await self.repo_area.obtener_por_id(id_area)
            if not area:
                raise AreaNoExisteError("No hay id de area")
            return [area]
        return await self.repo_areas.obtener_todos()
