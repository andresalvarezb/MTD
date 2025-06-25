from typing import Protocol
from core.entidades.areaMtd import AreaMTD


# class RepositorioAreaMTD(Protocol):
#     def guardar(self, AreaMTD: AreaMTD) -> AreaMTD: ...

class ObtenerAreaPorNombreProtocol(Protocol):
    def obtener_por_nombre(self, nombre_area: str) -> AreaMTD | None: ...