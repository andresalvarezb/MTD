from typing import Protocol, runtime_checkable
from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario

# from infraestructura.db.modelos.historialLaboralUsuario import HistorialLaboralORM


@runtime_checkable
class RepositorioHistorialLaboralUsuario(Protocol):
    def guardar(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario: ...
