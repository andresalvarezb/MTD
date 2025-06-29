from datetime import datetime
from dataclasses import dataclass
from core.entidades.cargo import Cargo
from core.entidades.usuario import Usuario
from core.entidades.municipio import Municipio
from infraestructura.db.modelos.historialLaboralUsuario import HistorialLaboralORM


@dataclass
class HistorialLaboralUsuario:
    usuario: Usuario
    contrato: str
    cargo: Cargo
    claveHLU: str
    municipio: Municipio
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
            id=orm_obj.id,
            municipio=Municipio.from_orm(orm_obj.municipio),
            contrato=orm_obj.contrato,
            cargo=Cargo.from_orm(orm_obj.cargo),
            fecha_contratacion=orm_obj.fecha_contratacion,
            claveHLU=orm_obj.claveHLU,
            usuario=Usuario.from_orm(orm_obj.usuario),
            seguridad_social=orm_obj.seguridad_social,
            fecha_aprobacion_seguridad_social=orm_obj.fecha_aprobacion_seguridad_social,
            fecha_ultima_contratacion=orm_obj.fecha_ultima_contratacion,
            fecha_fin_contratacion=orm_obj.fecha_fin_contratacion,
        )
