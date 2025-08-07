from sqlalchemy.ext.asyncio import AsyncSession
from core.entidades.usuario import Usuario
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update
from infraestructura.db.modelos.usuario import UsuarioORM
from infraestructura.db.modelos.municipio import MunicipioORM
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
        return Usuario.from_orm(usuario_nuevo)

    async def obtener_por_documento(self, documento: str) -> Usuario | None:
        try:
            registro_orm = await self.db.execute(
                select(UsuarioORM)
                .options(
                    selectinload(UsuarioORM.municipio).selectinload(MunicipioORM.departamento),
                    selectinload(UsuarioORM.cargo),
                )
                .where(UsuarioORM.documento == documento)
            )
            registro_orm = registro_orm.scalar_one_or_none()
            if registro_orm:
                return Usuario.from_orm(registro_orm)
            return None
        except Exception as e:
            print(f"Error al obtener usuario por documento: {e}")
            return None

    async def obtener_por_id(self, id_usuario: int) -> Usuario | None:
        registro_orm = await self.db.execute(
            select(UsuarioORM)
            .options(
                selectinload(UsuarioORM.municipio).selectinload(MunicipioORM.departamento),
                selectinload(UsuarioORM.cargo),
            )
            .where(UsuarioORM.id == id_usuario)
        )
        registro_orm = registro_orm.scalar_one_or_none()
        if not registro_orm:
            return None
        return Usuario.from_orm(registro_orm)

    async def obtener_todos(self) -> list[Usuario]:
        registros_orm = await self.db.execute(
            select(UsuarioORM).options(
                selectinload(UsuarioORM.municipio).selectinload(MunicipioORM.departamento),
                selectinload(UsuarioORM.cargo),
            )
        )
        registros_orm = registros_orm.scalars().all()
        return [Usuario.from_orm(registro_orm) for registro_orm in registros_orm]

    async def actualizar(self, info_nueva: dict, usuario: Usuario) -> Usuario:
        registro_orm = await self.db.execute(
            update(UsuarioORM)
            .where(UsuarioORM.id == usuario.id)
            .values(**info_nueva)
            .returning(UsuarioORM)  # <<--- Esto devuelve la fila actualizada como ORM
        )
        registro_orm = registro_orm.scalar_one_or_none()
        if not registro_orm:
            raise ValueError("Usuario no encontrado")

        # Sincronizar con la sesión (no guarda todavía)
        await self.db.flush()
        return Usuario.from_orm(registro_orm)
