from core.entidades.municipio import Municipio
from core.interfaces.repositorioMunicipio import CrearMunicipioProtocol, ObtenerMunicipioPorNombreProtocol
from core.servicios.municipio.dtos import CrearMunicipioDTO


class CrearMunicipio:
    def __init__(self, repo_municipio):
        self.repo_crear: CrearMunicipioProtocol = repo_municipio
        self.repo_obtener: ObtenerMunicipioPorNombreProtocol = repo_municipio

    async def ejecutar(self, datos: CrearMunicipioDTO) -> Municipio:
        municipio = Municipio(nombre=datos.nombre, departamento=datos.departamento)

        existe_municipio = await self.repo_obtener.obtener_por_nombre(municipio)
        if existe_municipio:
            return existe_municipio

        # crearlo de no existir
        nuevo_municipio = await self.repo_crear.crear(municipio)
        return nuevo_municipio
