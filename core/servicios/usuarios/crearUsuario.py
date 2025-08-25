from core.entidades.usuario import Usuario
from core.servicios.usuarios.dtos import CrearUsuarioDTO
from core.interfaces.repositorioUsuario import CrearUsuarioProtocol
from core.servicios.departamento.dtos import CrearDepartamentoDTO
from core.servicios.usuarios.obtenerUsuarios import ObtenerUsuarios
from core.servicios.cargos.crearCargo import CrearCargo
from core.servicios.cargos.dtos import CrearCargoDTO
from core.servicios.municipio.crearMunicipio import CrearMunicipio
from core.servicios.municipio.dtos import CrearMunicipioDTO
from core.servicios.utilities.exepciones import UsuarioNoExisteError


class CrearUsuario:
    def __init__(
        self,
        obtener_usuario: ObtenerUsuarios,
        crear_usuario_repo: CrearUsuarioProtocol,
        crear_cargo: CrearCargo,
        crear_municipio: CrearMunicipio,
    ):
        self.obtener_usuario = obtener_usuario
        self.crear_usuario_repo = crear_usuario_repo
        self.crear_cargo = crear_cargo
        self.crear_municipio = crear_municipio

    async def ejecutar(self, datos: CrearUsuarioDTO) -> Usuario:
        # Validar existencia de usuario
        try:
            usuario_existente = await self.obtener_usuario.ejecutar(datos.documento)
            return usuario_existente[0]
        except UsuarioNoExisteError:
            cargo = await self.crear_cargo.ejecutar(CrearCargoDTO(nombre=datos.cargo.nombre))

            municipio = await self.crear_municipio.ejecutar(
                CrearMunicipioDTO(
                    nombre=datos.municipio.nombre,
                    departamento=CrearDepartamentoDTO(nombre=datos.municipio.departamento.nombre),
                )
            )

            usuario = Usuario(
                documento=datos.documento,
                nombre=datos.nombre,
                estado=datos.estado,
                contrato=datos.contrato,
                cargo=cargo,
                municipio=municipio,
                correo=datos.correo,
                telefono=datos.telefono,
                seguridad_social=datos.seguridad_social,
                fecha_aprobacion_seguridad_social=datos.fecha_aprobacion_seguridad_social,
                fecha_ultima_contratacion=datos.fecha_ultima_contratacion,
            )

            return await self.crear_usuario_repo.crear(usuario)
