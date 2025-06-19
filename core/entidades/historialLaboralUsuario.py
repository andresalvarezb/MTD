from dataclasses import dataclass
from datetime import datetime


@dataclass
class HistorialLaboralUsuario:
    id: int
    id_usuario: int
    fecha_inico: datetime
    fecha_fin: datetime | None = None
