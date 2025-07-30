from sqlalchemy.ext.asyncio import AsyncSession
from core.entidades.usuario import Usuario
from sqlalchemy import select
from infraestructura.db.modelos.usuario import UsuarioORM
from core.interfaces.repositorioUsuario import (
    CrearUsuarioProtocol,
    ObtenerUsuarioPorIdProtocol,
    ObtenerUsuarioPorDocumentoProtocol,
    ObtenerUsuariosProtocol,
    ActualizarUsuarioProtocol,
)


class RepositorioUsuarioSqlAlchemy(
    CrearUsuarioProtocol,
    ObtenerUsuarioPorIdProtocol,
    ObtenerUsuarioPorDocumentoProtocol,
    ObtenerUsuariosProtocol,
    ActualizarUsuarioProtocol,
):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crear(self, usuario: Usuario) -> Usuario:
        usuario_nuevo = UsuarioORM(
            documento=usuario.documento,
            nombre=usuario.nombre,
            estado=usuario.estado,
            id_municipio=usuario.municipio.id,
            contrato=usuario.contrato,
            id_cargo=usuario.cargo.id,
            correo=usuario.correo,
            telefono=usuario.telefono,
            seguridad_social=usuario.seguridad_social,
            fecha_aprobacion_seguridad_social=usuario.fecha_aprobacion_seguridad_social,
            fecha_ultima_contratacion=usuario.fecha_ultima_contratacion,
        )
        self.db.add(usuario_nuevo)
        await self.db.flush()
        await self.db.refresh(usuario_nuevo)
        return usuario.from_orm(usuario_nuevo)

    async def obtener_por_documento(self, documento_usuario: str) -> Usuario | None:
        registro_orm = await self.db.execute(select(UsuarioORM).where(UsuarioORM.documento == documento_usuario))
        registro_orm = registro_orm.scalar_one_or_none()
        if registro_orm:
            return Usuario.from_orm(registro_orm)
        else:
            return None

    async def obtener_por_id(self, id_usuario: int) -> Usuario | None:
        registro_orm = await self.db.execute(select(UsuarioORM).where(UsuarioORM.id == id_usuario))
        registro_orm = registro_orm.scalar_one_or_none()
        if not registro_orm:
            return None
        return Usuario.from_orm(registro_orm)

    async def obtener_todos(self, documento: str | None = None) -> list[Usuario]:
        if documento:
            registro_orm = await self.db.execute(select(UsuarioORM).where(UsuarioORM.documento == documento))
            registro_orm = registro_orm.scalar_one_or_none()
            return [Usuario.from_orm(registro_orm)] if registro_orm else []
        else:
            registros_orm = await self.db.execute(select(UsuarioORM))
            registros_orm = registros_orm.scalars().all()
            return [Usuario.from_orm(registro_orm) for registro_orm in registros_orm]

    async def actualizar(self, usuario: Usuario) -> Usuario:
        registro_orm = await self.db.execute(select(UsuarioORM).where(UsuarioORM.id == usuario.id))
        registro_orm = registro_orm.scalar_one_or_none()
        if not registro_orm:
            raise ValueError("Usuario no encontrado")

        if not usuario.municipio.id:
            raise ValueError("Municipio no asociado al usuario")

        if not usuario.cargo.id:
            raise ValueError("Cargo no asociado al usuario")

        # Actualizar solo los campos que corresponden
        registro_orm.documento = usuario.documento
        registro_orm.nombre = usuario.nombre
        registro_orm.estado = usuario.estado
        registro_orm.contrato = usuario.contrato
        registro_orm.correo = usuario.correo
        registro_orm.telefono = usuario.telefono
        registro_orm.seguridad_social = usuario.seguridad_social
        registro_orm.fecha_aprobacion_seguridad_social = usuario.fecha_aprobacion_seguridad_social
        registro_orm.fecha_ultima_contratacion = usuario.fecha_ultima_contratacion
        registro_orm.id_municipio = usuario.municipio.id
        registro_orm.id_cargo = usuario.cargo.id

        # Sincronizar con la sesión (no guarda todavía)
        await self.db.flush()
        return Usuario.from_orm(registro_orm)
