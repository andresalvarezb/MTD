from pydantic import BaseModel
from datetime import datetime
from .usuario import UsuarioResponseSchema
from .banco import BancoResponseSchema




class CuentaBancariaResponseSchema(BaseModel):
    id: int
    numero_certificado: str
    numero_cuenta: str
    estado: str
    tipo_de_cuenta: str
    fecha_actualizacion: datetime
    observaciones: str
    banco: BancoResponseSchema
    usuario: UsuarioResponseSchema

    model_config = {"from_attributes": True}