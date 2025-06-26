from typing import Protocol
from core.entidades.municipio import Municipio


class CrearMunicipioProtocol(Protocol):
    def crear(self, municipio: Municipio) -> Municipio: ...


class ObtenerMunicipioPorNombreProtocol(Protocol):
    def obtener_por_nombre(self, municipio: Municipio) -> Municipio | None: ...


class ObtenerMunicipioPorIdProtocol(Protocol):
    def obtener_por_id(self, id_municipio: int) -> Municipio | None: ...
