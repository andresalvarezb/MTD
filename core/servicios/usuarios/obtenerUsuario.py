from core.interfaces.repositorioUsuario import ObtenerUsuarioPorIdProtocol


class ObtenerUsuario:
    def __init__(self, repositorio_usuario: ObtenerUsuarioPorIdProtocol):
        self.repositorio_usuario = repositorio_usuario

    def ejecutar(self, id_usuario: int):
        usuario = self.repositorio_usuario.obtener_por_id(id_usuario)
        if not usuario:
            raise ValueError(f"Usuario no encontrado")
        return usuario
