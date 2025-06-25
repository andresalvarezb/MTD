from core.entidades.usuario import Usuario
from typing import Protocol, runtime_checkable


class CrearUsuarioProtocol(Protocol):
    def crear(self, usuario: Usuario) -> Usuario: ...


class ObtenerUsuarioPorIdProtocol(Protocol):
    def obtener_por_id(self, id_usuario: int) -> Usuario | None: ...


class ObtenerUsuarioPorDocumentoProtocol(Protocol):
    def obtener_por_documento(self, documento_usuario: str) -> Usuario | None: ...


class ActulizarSeguridadSocialUsuarioProtocol(Protocol):
    def actualizar_seguridad_social(self, usuario: Usuario) -> Usuario: ...

class ObtenerUsuariosProtocol(Protocol):
    def obtener_todos(self) -> list[Usuario]: ...


# class ActulizarSeguridadSocialUsuarioProtocol(Protocol):
#     def obtener_por_documento(self, documento_usuario: str) -> Usuario | None: ...
#     def actualizar_seguridad_social(self, usuario: Usuario) -> Usuario: ...
