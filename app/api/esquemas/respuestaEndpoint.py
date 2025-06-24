from pydantic import BaseModel


class WrapperRespuesta(BaseModel):
    mensaje: str
    status_code: int
    data: dict | list | str | None
