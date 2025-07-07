from core.interfaces.repositorioUsuario import ObtenerUsuariosProtocol


class ObtenerUsuarios:
    def __init__(self, repositorio_usuario: ObtenerUsuariosProtocol):
        self.repositorio_usuario = repositorio_usuario

    def ejecutar(self, documento: str | None = None):
        return self.repositorio_usuario.obtener_todos(documento)
