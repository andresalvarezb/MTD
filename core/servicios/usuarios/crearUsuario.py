from core.entidades.usuario import Usuario
from core.interfaces.repositorioUsuario import CrearUsuarioProtocol, ObtenerUsuarioPorDocumentoProtocol
from core.servicios.usuarios.dtos import CrearUsuarioDTO


class CrearUsuario:
    def __init__(self, repo_obtener: ObtenerUsuarioPorDocumentoProtocol, repo_crear: CrearUsuarioProtocol):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    def ejecutar(self, datos: CrearUsuarioDTO) -> Usuario:

        usuario = Usuario(
            documento=datos.documento,
            nombre=datos.nombre,
            estado=datos.estado,
            id_municipio=datos.id_municipio,
            contrato=datos.contrato,
            id_cargo=datos.id_cargo,
            correo=datos.correo,
            telefono=datos.telefono,
            seguridad_social=datos.seguridad_social,
            fecha_aprobacion_seguridad_social=datos.fecha_aprobacion_seguridad_social,
            fecha_ultima_contratacion=datos.fecha_ultima_contratacion,
        )

        usuario_existente = self.repo_obtener.obtener_por_documento(usuario.documento)
        if usuario_existente:
            return usuario_existente

        usuario_nuevo = self.repo_crear.crear(usuario)

        return usuario_nuevo
