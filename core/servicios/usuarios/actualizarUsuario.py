from core.interfaces.repositorioUsuario import ActualizarUsuarioProtocol, ObtenerUsuarioPorDocumentoProtocol
from core.servicios.usuarios.dtos import ActualizarUsuarioDTO
from core.entidades.usuario import Usuario
from dataclasses import asdict

# from app.api.esquemas.usuario import UsuarioUpdateSchema


class ActualizarUsuario:
    def __init__(self, repo_actualizar: ActualizarUsuarioProtocol, repo_obtener: ObtenerUsuarioPorDocumentoProtocol):
        self.repo_actualizar = repo_actualizar
        self.repo_obtener = repo_obtener

    async def ejecutar(self, info_nueva: ActualizarUsuarioDTO):

        usuario_existente = await self.repo_obtener.obtener_por_documento(info_nueva.documento)
        if not usuario_existente:
            raise ValueError("Usuario no encontrado. No se puede actualizar")

        usuario_actualizado = await self.repo_actualizar.actualizar(asdict(info_nueva), usuario_existente)

        return usuario_actualizado
