from dataclasses import asdict
from core.entidades.usuario import Usuario
from core.entidades.cargo import Cargo
from core.entidades.municipio import Municipio
from core.entidades.departamento import Departamento
from core.servicios.usuarios.dtos import CrearUsuarioDTO
from core.interfaces.repositorioUsuario import CrearUsuarioProtocol, ObtenerUsuarioPorDocumentoProtocol
from core.interfaces.repositorioMunicipio import CrearMunicipioProtocol, ObtenerMunicipioPorNombreProtocol
from core.interfaces.repositorioDepartamento import CrearDepartamentoProtocol, ObtenerDepartamentoPorNombreProtocol
from core.interfaces.repositorioCargo import CrearCargoProtocol, ObtenerCargoPorNombreProtocol


class CrearUsuario:
    def __init__(
        self,
        repo_obtener_usuario: ObtenerUsuarioPorDocumentoProtocol,
        repo_crear_usuario: CrearUsuarioProtocol,
        repo_obtener_municipio: ObtenerMunicipioPorNombreProtocol,
        repo_crear_municipio: CrearMunicipioProtocol,
        repo_obtener_departamento: ObtenerDepartamentoPorNombreProtocol,
        repo_crear_departamento: CrearDepartamentoProtocol,
        repo_obtener_cargo: ObtenerCargoPorNombreProtocol,
        repo_crear_cargo: CrearCargoProtocol,
    ):
        self.repo_crear_usuario = repo_crear_usuario
        self.repo_obtener_usuario = repo_obtener_usuario
        self.repo_obtener_municipio = repo_obtener_municipio
        self.repo_crear_municipio = repo_crear_municipio
        self.repo_obtener_departamento = repo_obtener_departamento
        self.repo_crear_departamento = repo_crear_departamento
        self.repo_obtener_cargo = repo_obtener_cargo
        self.repo_crear_cargo = repo_crear_cargo

    async def ejecutar(self, datos: CrearUsuarioDTO) -> Usuario:
        # Validar existencia de usuario
        usuario_existente = await self.repo_obtener_usuario.obtener_por_documento(datos.documento)
        if usuario_existente:
            return usuario_existente

        cargo_existente = await self.repo_obtener_cargo.obtener_por_nombre(datos.cargo.nombre)
        if not cargo_existente:
            cargo_existente = await self.repo_crear_cargo.crear(Cargo(datos.cargo.nombre))

        departamento_existente = await self.repo_obtener_departamento.obtener_por_nombre(
            datos.municipio.departamento.nombre
        )
        if not departamento_existente:
            departamento_existente = await self.repo_crear_departamento.crear(
                Departamento(datos.municipio.departamento.nombre)
            )

        municipio_existente = await self.repo_obtener_municipio.obtener_por_nombre(datos.municipio.nombre)
        if not municipio_existente:
            municipio_existente = await self.repo_crear_municipio.crear(
                Municipio(nombre=datos.municipio.nombre, departamento=departamento_existente)
            )

        usuario = Usuario(
            documento=datos.documento,
            nombre=datos.nombre,
            estado=datos.estado,
            contrato=datos.contrato,
            cargo=cargo_existente,
            municipio=municipio_existente,
            correo=datos.correo,
            telefono=datos.telefono,
            seguridad_social=datos.seguridad_social,
            fecha_aprobacion_seguridad_social=datos.fecha_aprobacion_seguridad_social,
            fecha_ultima_contratacion=datos.fecha_ultima_contratacion,
        )
        # print(usuario)
        usuario_nuevo = await self.repo_crear_usuario.crear(usuario)

        return usuario_nuevo


#     Cuando el usuario ya existe (y el caso de uso debería retornarlo sin crear nada).

# Cuando el cargo existe, pero municipio/departamento no (y viceversa).

# Casos de error (ej. datos inválidos si tu DTO o el caso de uso los validan).
