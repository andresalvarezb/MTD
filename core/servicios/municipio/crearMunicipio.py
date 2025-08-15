from core.entidades.municipio import Municipio
from core.interfaces.repositorioMunicipio import CrearMunicipioProtocol
from core.servicios.municipio.dtos import CrearMunicipioDTO, ObtenerMunicipioDTO
from core.servicios.municipio.ObtenerMunicipio import ObtenerMunicipio
from core.servicios.departamento.crearDepartamento import CrearDepartamento
from core.servicios.departamento.dtos import CrearDepartamentoDTO
from core.servicios.utilities.exepciones import MunicipioNoExisteError

class CrearMunicipio:
    def __init__(
        self,
        obtener_municipio: ObtenerMunicipio,
        crear_municipio_repo: CrearMunicipioProtocol,
        crear_departamento: CrearDepartamento
    ):
        self.obtener_municipio = obtener_municipio
        self.crear_municipio_repo = crear_municipio_repo
        self.crear_departamento = crear_departamento

    async def ejecutar(self, datos: CrearMunicipioDTO) -> Municipio:
        try:
            return await self.obtener_municipio.ejecutar(
                ObtenerMunicipioDTO(nombre=datos.nombre)
            )
        except MunicipioNoExisteError:
            departamento = await self.crear_departamento.ejecutar(
                CrearDepartamentoDTO(nombre=datos.departamento.nombre)
            )
            municipio = Municipio(nombre=datos.nombre, departamento=departamento)
            return await self.crear_municipio_repo.crear(municipio)