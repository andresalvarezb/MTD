from core.entidades.usuario import Usuario
from core.interfaces.repositorioUsuario import RepositorioUsuario


class CrearUsuario:
    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio

    def ejecutar(self, datos: dict) -> Usuario:
        usuario = Usuario(
            documento=datos["documento"],
            nombre=datos["nombre"],
            estado=datos["estado"],
            id_municipio=datos["id_municipio"],
            contrato=datos["contrato"],
            id_cargo=datos["id_cargo"],
            correo=datos["correo"],
            telefono=datos["telefono"],
            seguridad_social=datos["seguridad_social"],
            fecha_aprobacion_seguridad_social=datos["fecha_aprobacion_seguridad_social"],
            fecha_ultima_contratacion=datos["fecha_ultima_contratacion"],
        )

        usuario = self.repositorio.guardar(usuario)

        return usuario
