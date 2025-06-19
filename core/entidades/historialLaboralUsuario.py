from datetime import datetime
from dataclasses import dataclass


@dataclass
class HistorialLaboralUsuario:
    id_municipio: int
    contrato: str
    id_cargo: int
    fecha_contratacion: datetime
    claveHLU: str
    id_usuario: int
    id: int | None = None
    seguridad_social: bool | None = None
    fecha_aprobacion_seguridad_social: datetime | None = None
    fecha_ultima_contratacion: datetime | None = None
    fecha_fin_contratacion: datetime | None = None

    def __post_init__(self):
        if self.fecha_fin_contratacion and self.fecha_fin_contratacion < self.fecha_contratacion:
            raise ValueError("La fecha de finalizacion de contrato no puede ser menor a la fecha de contratación")
