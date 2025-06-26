from pydantic import BaseModel
from datetime import datetime
from .municipio import MunicipioResponseSchema
from .cargo import CargoResponseSchema



class UsuarioResponseSchema(BaseModel):
    id: int
    documento: str
    nombre: str
    estado: str
    contrato: str
    correo: str
    telefono: str
    seguridad_social: bool
    fecha_ultima_contratacion: datetime
    fecha_aprobacion_seguridad_social: datetime
    cargo: CargoResponseSchema
    municipio: MunicipioResponseSchema


    model_config = {"from_attributes": True}