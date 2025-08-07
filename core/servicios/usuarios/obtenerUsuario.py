from core.interfaces.repositorioUsuario import ObtenerUsuarioPorDocumentoProtocol
from core.entidades.usuario import Usuario


class ObtenerUsuario:
    def __init__(self, repositorio_usuario: ObtenerUsuarioPorDocumentoProtocol):
        self.repositorio_usuario = repositorio_usuario

    async def ejecutar(self, documento: str) -> Usuario:
        usuario = await self.repositorio_usuario.obtener_por_documento(documento)
        if not usuario:
            raise ValueError(f"Usuario no encontrado")
        return usuario
