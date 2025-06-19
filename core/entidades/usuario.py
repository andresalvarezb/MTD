from dataclasses import dataclass
from datetime import datetime

@dataclass
class Usuario:
    id: int
    documento: str
    nombre: str
    estado: str
    id_municipio: int
    contrato: str
    cargo: str
    correo: str | None = None
    telefono: str | None = None
    seguridad_social: bool | None = None
    fecha_aprobacion_seguridad_social: datetime | None = None