from pydantic import BaseModel
from datetime import datetime


class ActualizacionSeguridadSocialSchema(BaseModel):
    id_usuario: int
    id_cuenta_por_pagar: int
    documento_usuario: str
    tiene_seguridad_social: bool
    fecha_aprobacion_seguridad_social: datetime