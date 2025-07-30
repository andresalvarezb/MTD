from core.interfaces.repositorioAreaMTD import ObtnerAreaPorIdProtocol


class ObtenerAreaMTD:
    def __init__(self, repo_obtener: ObtnerAreaPorIdProtocol):
        self.repo_obtener = repo_obtener

    async def ejecutar(self, id_area: int):

        if not id_area:
            raise ValueError("No hay id de area")

        area = await self.repo_obtener.obtener_por_id(id_area)

        if not area:
            raise ValueError("Area no encontrada")

        return area
