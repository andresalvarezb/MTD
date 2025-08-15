from core.entidades.municipio import Municipio
from core.interfaces.repositorioMunicipio import CrearMunicipioProtocol, ObtenerMunicipioPorNombreProtocol
from core.servicios.municipio.dtos import CrearMunicipioDTO, ObtenerMunicipioDTO
from core.servicios.municipio.ObtenerMunicipio import ObtenerMunicipio


class CrearMunicipio:
    def __init__(self, repo_municipio):
        self.repo_crear: CrearMunicipioProtocol = repo_municipio
        self.repo_obtener: ObtenerMunicipioPorNombreProtocol = repo_municipio

    async def ejecutar(self, datos: CrearMunicipioDTO) -> Municipio:
        try:
            existe_municipio = await ObtenerMunicipio(self.repo_obtener).ejecutar(
                ObtenerMunicipioDTO(nombre=datos.nombre)
            )
            return existe_municipio
        except ValueError:
            municipio = Municipio(nombre=datos.nombre, departamento=datos.departamento)
            return await self.repo_crear.crear(municipio)
