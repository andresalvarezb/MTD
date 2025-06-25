from dataclasses import dataclass
from datetime import datetime



@dataclass
class CrearBancoDTO:
    nombre: str

@dataclass
class CrearCuentaBancariaDTO:
    numero_cuenta: str
    numero_certificado: str | None
    estado: str
    id_usuario: int
    id_banco: int
    tipo_de_cuenta: str | None
    fecha_actualizacion: datetime | None
    observaciones: str | None