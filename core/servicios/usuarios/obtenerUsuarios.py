from core.entidades.usuario import Usuario
from core.servicios.utilities.exepciones import UsuarioNoExisteError
from core.interfaces.repositorioUsuario import ObtenerUsuariosProtocol, ObtenerUsuarioPorDocumentoProtocol


class ObtenerUsuarios:
    def __init__(self, repo_usuarios: ObtenerUsuariosProtocol, repo_usuario: ObtenerUsuarioPorDocumentoProtocol):
        self.repositorio_usuarios = repo_usuarios
        self.repositorio_usuario = repo_usuario

    async def ejecutar(self, documento: str | None = None) -> list[Usuario]:
        if documento:
            usuario = await self.repositorio_usuario.obtener_por_documento(documento)
            if not usuario:
                raise UsuarioNoExisteError(f"Usuario no encontrado")
            return [usuario]
        return await self.repositorio_usuarios.obtener_todos()
