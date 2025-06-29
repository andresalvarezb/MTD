from core.entidades.cargo import Cargo
from core.servicios.usuarios.dtos import CrearCargoDTO
from core.interfaces.repositorioCargo import CrearCargoProtocol, ObtenerCargoPorNombreProtocol


class CrearCargo:
    def __init__(self, repo_crear: CrearCargoProtocol, repo_obtener: ObtenerCargoPorNombreProtocol):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    def ejecutar(self, datos: CrearCargoDTO) -> Cargo:
        # obtener cargo
        cargo = Cargo(nombre=datos.nombre)
        cargo_existente = self.repo_obtener.obtener_por_nombre(cargo)

        if cargo_existente:
            return cargo_existente

        # Crear cargo
        cargo_nuevo = self.repo_crear.crear(cargo)
        return cargo_nuevo
