from pydantic import BaseModel
from .usuario import UsuarioResponseSchema
from .municipio import MunicipioResponseSchema
from .cargo import CargoResponseSchema



class HistorialLaboralResponseSchema(BaseModel):
    id: int
    claveHLU: str
    contrato: str
    seguridad_social: bool
    fecha_contratacion: str
    fecha_fin_contratacion: str
    fecha_aprobacion_seguridad_social: str
    fecha_ultima_contratacion: str
    usuario: UsuarioResponseSchema
    municipio: MunicipioResponseSchema
    cargo: CargoResponseSchema

    model_config = {"from_attributes": True}