from core.interfaces.repositorioAreaMTD import EliminarAreaMTDProtocol


class EliminarAreaMTD:
    def __init__(self, repositorio_area: EliminarAreaMTDProtocol):
        self.repositorio_area = repositorio_area

    async def ejecutar(self, id_area: int):
        return await self.repositorio_area.eliminar(id_area)
