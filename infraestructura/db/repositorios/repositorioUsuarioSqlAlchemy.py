from sqlalchemy.orm import Session
from core.entidades.usuario import Usuario
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
    def __init__(self, db: Session):
        self.db = db

    def crear(self, usuario: Usuario) -> Usuario:
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
        self.db.flush()
        self.db.refresh(usuario_nuevo)
        return usuario.from_orm(usuario_nuevo)

    def obtener_por_documento(self, documento_usuario: str) -> Usuario | None:
        registro_orm = self.db.query(UsuarioORM).filter_by(documento=documento_usuario).first()
        if registro_orm:
            return Usuario.from_orm(registro_orm)
        else:
            return None

    def obtener_por_id(self, id_usuario: int) -> Usuario | None:
        registro_orm = self.db.query(UsuarioORM).filter_by(id=id_usuario).first()
        if not registro_orm:
            return None
        return Usuario.from_orm(registro_orm)

    def obtener_todos(self) -> list[Usuario]:
        registros_orm = self.db.query(UsuarioORM).all()
        return [Usuario.from_orm(registro_orm) for registro_orm in registros_orm]

    def actualizar(self, usuario: Usuario) -> Usuario:
        registro_orm = self.db.query(UsuarioORM).filter_by(id=usuario.id).first()
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
        self.db.flush()
        return Usuario.from_orm(registro_orm)
