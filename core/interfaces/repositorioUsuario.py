from core.entidades.usuario import Usuario
from typing import Protocol, runtime_checkable


@runtime_checkable
class RepositorioUsuario(Protocol):
    def guardar(self, usuario: Usuario) -> Usuario: ...
