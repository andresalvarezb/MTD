from core.interfaces.repositorioHistorialLaboralUsuario import (
    ActualizarHistorialLaboralUsuarioProtocol,
    ObtenerHistorialLaboralPorIdProtocol,
)
from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario
from app.api.esquemas.historialLaboralUsuario import HistorialLaboralUpdateSchema
from core.servicios.historialLaboral.dtos import ActualizarHistorialLaboralUsuarioDTO


class ActualizarHistorialLaboral:
    def __init__(
        self,
        repo_actualizar: ActualizarHistorialLaboralUsuarioProtocol,
        repo_obtener: ObtenerHistorialLaboralPorIdProtocol,
    ):
        self.repo_actualizar = repo_actualizar
        self.repo_obtener = repo_obtener

    def ejecutar(self, info_nueva: ActualizarHistorialLaboralUsuarioDTO, info_vieja: HistorialLaboralUsuario):

        for key, value in info_nueva.__dict__.items():
            setattr(info_vieja, key, value)

        historial_actualizado = self.repo_actualizar.actualizar(info_vieja)

        return historial_actualizado
