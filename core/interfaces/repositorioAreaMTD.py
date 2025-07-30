from typing import Protocol
from core.entidades.areaMtd import AreaMTD


class CrearAreaMTDProtocol(Protocol):
    async def crear(self, area: AreaMTD) -> AreaMTD: ...


class ObtenerAreaPorNombreProtocol(Protocol):
    async def obtener_por_nombre(self, nombre_area: str) -> AreaMTD | None: ...


class ObtenerAreasProtocol(Protocol):
    async def obtener_todos(self) -> list[AreaMTD]: ...


class ObtnerAreaPorIdProtocol(Protocol):
    async def obtener_por_id(self, id_area: int) -> AreaMTD | None: ...


class EliminarAreaMTDProtocol(Protocol):
    async def eliminar(self, id_area: int) -> None: ...
