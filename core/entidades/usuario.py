import re
from datetime import datetime
from dataclasses import dataclass
from core.entidades.cargo import Cargo
from core.entidades.municipio import Municipio
from infraestructura.db.modelos.usuario import UsuarioORM
from utils.enums import EnumEstadoUsuario, EnumTipoContrato


EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


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
        # Validar documento
        if not self.documento.isdigit() or not (4 <= len(self.documento) <= 12):
            raise ValueError("El documento debe tener entre 4 y 12 dígitos numéricos.")

        # Validar nombre
        self.nombre = self.nombre.strip().upper()
        if not self.nombre or len(self.nombre) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")

        # Validar estado
        self.estado = self.estado.strip().upper()
        if self.estado not in [item.value for item in EnumEstadoUsuario]:
            raise ValueError("El estado debe ser 'ACTIVO' o 'INACTIVO'.")

        # Validar contrato
        self.contrato = self.contrato.strip().upper()
        if (
            not self.contrato
            or len(self.contrato) < 3
            or self.contrato not in [item.value for item in EnumTipoContrato]
        ):
            raise ValueError("El contrato debe tener al menos 3 caracteres y ser 'OPS' o 'NOMINA'.")

        # Normalizar nombre
        # Validar correo (si viene)
        if self.correo and not EMAIL_REGEX.match(self.correo):
            raise ValueError("El correo electrónico no es válido.")

        # Validar teléfono (si viene)
        if self.telefono:
            if not self.telefono.isdigit() or len(self.telefono) not in (7, 10):
                raise ValueError("El teléfono debe tener 7 (fijo) o 10 (celular) dígitos numéricos.")

        if self.seguridad_social and not self.fecha_aprobacion_seguridad_social:
            raise ValueError("Debe proporcionar la fecha de aprobación si la seguridad social está activa.")

        if self.fecha_aprobacion_seguridad_social and self.fecha_ultima_contratacion:
            if self.fecha_aprobacion_seguridad_social > self.fecha_ultima_contratacion:
                raise ValueError("La fecha de aprobación no puede ser posterior a la contratación.")

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
