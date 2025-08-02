from core.interfaces.repositorioUsuario import ActualizarUsuarioProtocol, ObtenerUsuarioPorIdProtocol
from core.servicios.usuarios.dtos import ActualizarUsuarioDTO
from core.entidades.usuario import Usuario
from dataclasses import asdict
# from app.api.esquemas.usuario import UsuarioUpdateSchema


class ActualizarUsuario:
    def __init__(
        self,
        repo_actualizar: ActualizarUsuarioProtocol,
        #  repo_obtener: ObtenerUsuarioPorIdProtocol
    ):
        self.repo_actualizar = repo_actualizar
        # self.repo_obtener = repo_obtener

    # async def ejecutar(self, info_nueva: ActualizarUsuarioDTO, info_vieja: Usuario):

    #     for key, value in asdict(info_nueva).items():
    #         setattr(info_vieja, key, value)

    #     usuario_actualizado = await self.repo_actualizar.actualizar(info_vieja)

    #     return usuario_actualizado
    async def ejecutar(self, info_nueva: ActualizarUsuarioDTO, info_vieja: Usuario):

        # for key, value in asdict(info_nueva).items():
        #     setattr(info_vieja, key, value)

        usuario_actualizado = await self.repo_actualizar.actualizar(info_nueva.__dict__, info_vieja)

        return usuario_actualizado
