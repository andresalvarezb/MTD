from typing import Protocol, runtime_checkable
from core.entidades.municipio import Municipio, Departamento


@runtime_checkable
class RepositorioMunicipio(Protocol):
    def guardar(self, municipio: Municipio) -> Municipio: ...


@runtime_checkable
class RepositorioDepartamento(Protocol):
    def guardar(self, departamento: Departamento) -> Departamento: ...
