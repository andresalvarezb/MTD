from datetime import datetime
from dataclasses import dataclass

from infraestructura.db.modelos.historialLaboralUsuario import HistorialLaboralORM


@dataclass
class HistorialLaboralUsuario:
    id_municipio: int
    contrato: str
    id_cargo: int
    claveHLU: str
    id_usuario: int
    id: int | None = None
    fecha_contratacion: datetime | None = None
    seguridad_social: bool | None = None
    fecha_aprobacion_seguridad_social: datetime | None = None
    fecha_ultima_contratacion: datetime | None = None
    fecha_fin_contratacion: datetime | None = None

    def __post_init__(self):
        if (
            self.fecha_fin_contratacion
            and self.fecha_contratacion
            and self.fecha_fin_contratacion < self.fecha_contratacion
        ):
            raise ValueError("La fecha de finalizacion de contrato no puede ser menor a la fecha de contratación")

    @classmethod
    def from_orm(cls, orm_obj: HistorialLaboralORM) -> "HistorialLaboralUsuario":
        return cls(
            id_municipio=orm_obj.id_municipio,
            contrato=orm_obj.contrato,
            id_cargo=orm_obj.id_cargo,
            fecha_contratacion=orm_obj.fecha_contratacion,
            claveHLU=orm_obj.claveHLU,
            id_usuario=orm_obj.id_usuario,
            id=orm_obj.id,
            seguridad_social=orm_obj.seguridad_social,
            fecha_aprobacion_seguridad_social=orm_obj.fecha_aprobacion_seguridad_social,
            fecha_ultima_contratacion=orm_obj.fecha_ultima_contratacion,
            fecha_fin_contratacion=orm_obj.fecha_fin_contratacion,
        )
