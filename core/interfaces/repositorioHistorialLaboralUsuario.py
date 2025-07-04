from typing import Protocol, runtime_checkable
from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario


class CrearHistorialLaboralUsuarioProtocol(Protocol):
    def crear(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario: ...


class ObtenerHistorialLaboralPorIdProtocol(Protocol):
    def obtener_por_id(self, id_historial_laboral: int) -> HistorialLaboralUsuario | None: ...


class ObtenerHistorialLaboralPorClaveProtocol(Protocol):
    def obtener_por_clave(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario | None: ...


class ActualizarHistorialLaboralUsuarioProtocol(Protocol):
    def actualizar(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario: ...
