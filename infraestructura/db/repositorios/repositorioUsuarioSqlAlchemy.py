from sqlalchemy.orm import Session
from core.entidades.usuario import Usuario
from infraestructura.db.modelos.usuario import UsuarioORM
from core.interfaces.repositorioUsuario import CrearUsuarioProtocol, ObtenerUsuarioPorIdProtocol, ObtenerUsuarioPorDocumentoProtocol, ObtenerUsuariosProtocol


class RepositorioUsuarioSqlAlchemy(CrearUsuarioProtocol, ObtenerUsuarioPorIdProtocol, ObtenerUsuarioPorDocumentoProtocol, ObtenerUsuariosProtocol):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, usuario: Usuario) -> Usuario:
        """Implementación para guardar un usuario en la base de datos"""

        # verificar existencia
        registro_orm = self.db.query(UsuarioORM).filter_by(documento=usuario.documento).first()
        if registro_orm:
            usuario.id = registro_orm.id
            return usuario

        # creacion
        nuevo_usuario = UsuarioORM(**usuario.__dict__)
        self.db.add(nuevo_usuario)
        self.db.flush()
        self.db.refresh(nuevo_usuario)

        usuario.id = nuevo_usuario.id
        return usuario

    def obtener_por_documento(self, documento_usuario: str):
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

    def actualizar_seguridad_social(self, usuario: Usuario):
        registro_orm = self.db.query(UsuarioORM).filter_by(id=usuario.id).first()
        if not registro_orm:
            raise ValueError("Usuario no encontrado")
        registro_orm.seguridad_social = usuario.seguridad_social
        return Usuario.from_orm(registro_orm)
    
    def obtener_todos(self) -> list[Usuario]:
        registros_orm = self.db.query(UsuarioORM).all()
        return [Usuario.from_orm(registro_orm) for registro_orm in registros_orm]