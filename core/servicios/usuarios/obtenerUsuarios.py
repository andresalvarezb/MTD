from core.interfaces.repositorioUsuario import ObtenerUsuariosProtocol


class ObtenerUsuarios:
    def __init__(self, repositorio_usuario: ObtenerUsuariosProtocol):
        self.repositorio_usuario = repositorio_usuario

    async def ejecutar(self, documento: str | None = None):
        return await self.repositorio_usuario.obtener_todos(documento)
