from dataclasses import asdict
from core.entidades.usuario import Usuario
from core.servicios.usuarios.dtos import CrearUsuarioDTO
from core.interfaces.repositorioUsuario import CrearUsuarioProtocol, ObtenerUsuarioPorDocumentoProtocol


class CrearUsuario:
    def __init__(self, repo_obtener: ObtenerUsuarioPorDocumentoProtocol, repo_crear: CrearUsuarioProtocol):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    async def ejecutar(self, datos: CrearUsuarioDTO) -> Usuario:

        usuario = Usuario(**asdict(datos))

        # Validar existencia de usuario
        usuario_existente = await self.repo_obtener.obtener_por_documento(usuario.documento)
        if usuario_existente:
            return usuario_existente

        usuario_nuevo = await self.repo_crear.crear(usuario)

        return usuario_nuevo

        # usuario = Usuario(
        #     documento=datos.documento,
        #     nombre=datos.nombre,
        #     estado=datos.estado,
        #     municipio=datos.municipio,
        #     contrato=datos.contrato,
        #     cargo=datos.cargo,
        #     correo=datos.correo,
        #     telefono=datos.telefono,
        #     seguridad_social=datos.seguridad_social,
        #     fecha_aprobacion_seguridad_social=datos.fecha_aprobacion_seguridad_social,
        #     fecha_ultima_contratacion=datos.fecha_ultima_contratacion,
        # )