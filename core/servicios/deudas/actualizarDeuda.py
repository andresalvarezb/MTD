from core.interfaces.repositorioDeuda import ActualizarDeudaProtocol, ObtenerDeudaPorIdProtocol
from core.entidades.deuda import Deuda

# from core.servicios.deudas.dtos import ActualizarDeudaDTO
from app.api.esquemas.deuda import ActualizarDeudaSchema


class ActualizarDeuda:
    def __init__(self, repo_obtener: ObtenerDeudaPorIdProtocol, repo_actualizar: ActualizarDeudaProtocol):
        self.repo_obtener = repo_obtener
        self.repo_actualizar = repo_actualizar

    def ejecutar(self, id_deuda: int, info_nueva: ActualizarDeudaSchema) -> Deuda:
        info_vieja = self.repo_obtener.obtener_por_id(id_deuda)

        if not info_vieja:
            raise ValueError(f"La deuda con ID {id_deuda} no existe.")

        for key, value in info_nueva.__dict__.items():
            setattr(info_vieja, key, value)

        # TODO: Traer los descuentos asociados a esta deuda y recalcular el saldo y el estado

        deuda = self.repo_actualizar.actualizar(info_vieja)

        return deuda
