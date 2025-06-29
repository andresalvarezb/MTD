from typing import Protocol
from core.entidades.departamento import Departamento


class CrearDepartamentoProtocol(Protocol):
    def crear(self, departamento: Departamento) -> Departamento: ...


class ObtenerDepartamentoPorNombreProtocol(Protocol):
    def obtener_por_nombre(self, departamento: Departamento) -> Departamento | None: ...


class ObtenerDepartamentoPorIdProtocol(Protocol):
    def obtener_por_id(self, id_departamento: int) -> Departamento | None: ...
