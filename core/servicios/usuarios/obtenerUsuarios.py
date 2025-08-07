from core.interfaces.repositorioUsuario import ObtenerUsuariosProtocol


class ObtenerUsuarios:
    def __init__(self, repositorio_usuario: ObtenerUsuariosProtocol):
        self.repositorio_usuario = repositorio_usuario

    async def ejecutar(self):
        return await self.repositorio_usuario.obtener_todos()
