from dataclasses import dataclass
from datetime import datetime


@dataclass
class Usuario:
    documento: str
    nombre: str
    estado: str
    id_municipio: int
    contrato: str
    id_cargo: int
    id: int | None = None
    correo: str | None = None
    telefono: str | None = None
    seguridad_social: bool | None = None
    fecha_aprobacion_seguridad_social: datetime | None = None
    fecha_ultima_contratacion: datetime | None = None

    def __post_init__(self):
        self.nombre = self.nombre.upper()
        self.contrato = self.contrato.upper()
        self.estado = self.estado.upper()
        if self.correo:
            self.correo = self.correo.lower()

    def actualizar_seguridad_social(self, nueva_fecha: datetime):
        self.fecha_aprobacion_seguridad_social = nueva_fecha

        if nueva_fecha.month == datetime.now().month and nueva_fecha.year == datetime.now().year:
            self.seguridad_social = True
