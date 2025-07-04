from typing import Protocol
from core.entidades.areaMtd import AreaMTD


class CrearAreaMTDProtocol(Protocol):
    def crear(self, area: AreaMTD) -> AreaMTD: ...


class ObtenerAreaPorNombreProtocol(Protocol):
    def obtener_por_nombre(self, nombre_area: str) -> AreaMTD | None: ...


class ObtenerAreasProtocol(Protocol):
    def obtener_todos(self) -> list[AreaMTD]: ...


class ObtnerAreaPorIdProtocol(Protocol):
    def obtener_por_id(self, id_area: int) -> AreaMTD | None: ...


class EliminarAreaMTDProtocol(Protocol):
    def eliminar(self, id_area: int) -> None: ...
