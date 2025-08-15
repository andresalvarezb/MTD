from core.entidades.cargo import Cargo
from core.servicios.cargos.obtenerCargo import ObtenerCargo
from core.servicios.cargos.dtos import CrearCargoDTO, ObtenerCargoDTO
from core.interfaces.repositorioCargo import CrearCargoProtocol, ObtenerCargoPorNombreProtocol


class CrearCargo:
    def __init__(self, repo_crear: CrearCargoProtocol, repo_obtener: ObtenerCargoPorNombreProtocol):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    async def ejecutar(self, datos: CrearCargoDTO) -> Cargo:
        try:
            cargo_existente = await ObtenerCargo(self.repo_obtener).ejecutar(ObtenerCargoDTO(nombre=datos.nombre))
            return cargo_existente
        except ValueError:
            cargo_nuevo = await self.repo_crear.crear(Cargo(nombre=datos.nombre))
            return cargo_nuevo
