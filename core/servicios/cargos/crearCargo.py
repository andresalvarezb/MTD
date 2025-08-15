from core.entidades.cargo import Cargo
from core.servicios.cargos.obtenerCargo import ObtenerCargo
from core.servicios.cargos.dtos import CrearCargoDTO, ObtenerCargoDTO
from core.interfaces.repositorioCargo import CrearCargoProtocol
from core.servicios.utilities.exepciones import CargoNoExisteError

class CrearCargo:
    def __init__(self, repo_crear: CrearCargoProtocol, repo_obtener: ObtenerCargo):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    async def ejecutar(self, datos: CrearCargoDTO) -> Cargo:
        try:
            cargo_existente = await self.repo_obtener.ejecutar(ObtenerCargoDTO(nombre=datos.nombre))
            return cargo_existente
        except CargoNoExisteError:
            cargo_nuevo = await self.repo_crear.crear(Cargo(nombre=datos.nombre))
            return cargo_nuevo
