from typing import Protocol, runtime_checkable
from core.entidades.municipio import Municipio, Departamento

# * MUNICIPIO

class CrearMunicipioProtocol(Protocol):
    def crear(self, municipio: Municipio) -> Municipio: ...

class ObtenerMunicipioPorNombreProtocol(Protocol):
    def obtener_por_nombre(self, municipio: Municipio) -> Municipio | None: ...



# * DEPARTAMENTO
class CrearDepartamentoProtocol(Protocol):
    def crear(self, departamento: Departamento) -> Departamento: ...


class ObtenerDepartamentoPorNombreProtocol(Protocol):
    def obtener_por_nombre(self, departamento: Departamento) -> Departamento | None: ...
