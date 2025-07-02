from core.interfaces.repositorioCargo import ObtenerCargoPorNombreProtocol
from core.servicios.cargos.dtos import ObtenerCargoDTO
from core.entidades.cargo import Cargo


class ObtenerCargo:
    def __init__(self, repo_obtener: ObtenerCargoPorNombreProtocol):
        self.repo_obtener = repo_obtener

    def ejecutar(self, cargo: ObtenerCargoDTO):

        cargo_obtenido = self.repo_obtener.obtener_por_nombre(Cargo(nombre=cargo.nombre))

        if not cargo_obtenido:
            raise ValueError("Cargo no existe. Puede estar mal escrito o no creado")

        return cargo_obtenido
