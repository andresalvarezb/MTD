from datetime import datetime
from dataclasses import dataclass
from core.entidades.cargo import Cargo
from core.entidades.municipio import Municipio
from infraestructura.db.modelos.usuario import UsuarioORM


@dataclass
class Usuario:
    documento: str
    nombre: str
    estado: str
    contrato: str
    cargo: Cargo
    municipio: Municipio
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

    @classmethod
    def from_orm(cls, orm_obj: UsuarioORM) -> "Usuario":
        return cls(
            id=orm_obj.id,
            documento=orm_obj.documento,
            nombre=orm_obj.nombre,
            estado=orm_obj.estado,
            municipio=Municipio.from_orm(orm_obj.municipio),
            contrato=orm_obj.contrato,
            cargo=Cargo.from_orm(orm_obj.cargo),
            correo=orm_obj.correo,
            telefono=orm_obj.telefono,
            seguridad_social=orm_obj.seguridad_social,
            fecha_aprobacion_seguridad_social=orm_obj.fecha_aprobacion_seguridad_social,
            fecha_ultima_contratacion=orm_obj.fecha_ultima_contratacion,
        )
