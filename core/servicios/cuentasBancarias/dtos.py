from datetime import datetime
from dataclasses import dataclass
from core.entidades.banco import Banco
from core.entidades.usuario import Usuario


@dataclass
class CrearBancoDTO:
    nombre: str


@dataclass
class ObtenerBancoDTO:
    nombre: str


@dataclass
class CrearCuentaBancariaDTO:
    usuario: Usuario
    banco: Banco
    numero_cuenta: str
    numero_certificado: str | None
    estado: str
    tipo_de_cuenta: str | None
    fecha_actualizacion: datetime | None
    observaciones: str | None


@dataclass
class ActualizarCuentaBancariaDTO:
    usuario: Usuario | None
    banco: Banco | None
    numero_certificado: str | None
    estado: str | None
    tipo_de_cuenta: str | None
    observaciones: str | None
