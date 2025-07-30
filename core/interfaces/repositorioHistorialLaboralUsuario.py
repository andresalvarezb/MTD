from typing import Protocol
from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario


class CrearHistorialLaboralUsuarioProtocol(Protocol):
    async def crear(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario: ...


class ObtenerHistorialLaboralPorIdProtocol(Protocol):
    async def obtener_por_id(self, id_historial_laboral: int) -> HistorialLaboralUsuario | None: ...


class ObtenerHistorialLaboralPorClaveProtocol(Protocol):
    async def obtener_por_clave(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario | None: ...


class ActualizarHistorialLaboralUsuarioProtocol(Protocol):
    async def actualizar(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario: ...
