from core.servicios.municipio.dtos import ObtenerMunicipioDTO
from core.interfaces.repositorioMunicipio import ObtenerMunicipioPorNombreProtocol
from core.servicios.utilities.exepciones import MunicipioNoExisteError



class ObtenerMunicipio:
    def __init__(self, repo_obtener: ObtenerMunicipioPorNombreProtocol):
        self.repo_obtener = repo_obtener

    async def ejecutar(self, municipiodto: ObtenerMunicipioDTO):
        municipio_obtenido = await self.repo_obtener.obtener_por_nombre(municipiodto.nombre)
        if not municipio_obtenido:
            raise MunicipioNoExisteError("Municipio no encontrado. Puede estar mal escrito o no creado")
        return municipio_obtenido
