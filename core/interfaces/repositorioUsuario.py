from core.entidades.usuario import Usuario
from typing import Protocol, runtime_checkable


class CrearUsuarioProtocol(Protocol):
    async def crear(self, usuario: Usuario) -> Usuario: ...


class ObtenerUsuarioPorIdProtocol(Protocol):
    async def obtener_por_id(self, id_usuario: int) -> Usuario | None: ...


class ObtenerUsuarioPorDocumentoProtocol(Protocol):
    async def obtener_por_documento(self, documento_usuario: str) -> Usuario | None: ...


class ActulizarSeguridadSocialUsuarioProtocol(Protocol):
    async def actualizar_seguridad_social(self, usuario: Usuario) -> Usuario: ...


class ObtenerUsuariosProtocol(Protocol):
    async def obtener_todos(self, documento: str | None = None) -> list[Usuario]: ...


class ActualizarUsuarioProtocol(Protocol):
    async def actualizar(self, usuario: Usuario) -> Usuario: ...


# class ActulizarSeguridadSocialUsuarioProtocol(Protocol):
#     async def obtener_por_documento(self, documento_usuario: str) -> Usuario | None: ...
#     async def actualizar_seguridad_social(self, usuario: Usuario) -> Usuario: ...
