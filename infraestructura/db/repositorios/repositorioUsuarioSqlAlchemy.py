from sqlalchemy.orm import Session
from core.entidades.usuario import Usuario
from infraestructura.db.modelos.usuario import UsuarioORM
from core.interfaces.repositorioUsuario import RepositorioUsuario


class RepositorioUsuarioSqlAlchemy(RepositorioUsuario):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, usuario: Usuario) -> Usuario:
        """Implementación para guardar un usuario en la base de datos"""

        # verificar existencia
        existe = self.obtener(usuario)
        if existe:
            usuario.id = existe.id
            return usuario

        # creacion
        nuevo_usuario = UsuarioORM(**usuario.__dict__)
        self.db.add(nuevo_usuario)
        self.db.flush()
        self.db.refresh(nuevo_usuario)

        usuario.id = nuevo_usuario.id
        return usuario

    def obtener(self, usuario: Usuario):
        existe = self.db.query(UsuarioORM).filter_by(documento=usuario.documento).first()
        if existe:
            return existe
        else:
            return None
