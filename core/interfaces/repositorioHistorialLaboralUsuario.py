from typing import Protocol, runtime_checkable
from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario


class CrearHistorialLaboralUsuarioProtocol(Protocol):
    def guardar(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario: ...


class ObtenerHistorialLaboralPorIdProtocol(Protocol):
    def obtener_por_id(self, id_historial_laboral: int) -> HistorialLaboralUsuario | None: ...



class ActulizarSeguridadSocialHistorialLaboralProtocol(Protocol):
    # def obtener_por_id(self, id_historial_laboral: int) -> HistorialLaboralUsuario: ...
    def actualizar_seguridad_social(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario: ...