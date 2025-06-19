from sqlalchemy.orm import Session
from core.entidades.banco import Banco
from infraestructura.db.modelos.banco import BancoORM
from core.interfaces.repositorioBanco import RepositorioBanco


class RepositorioBancoSqlAlchemy(RepositorioBanco):
    def __init__(self, db: Session) -> None:
        self.db = db

    def guardar(self, banco: Banco) -> Banco:
        """Implementación para guardar el Banco en la base de datos"""

        # verificar existencia
        existe = self.obtener(banco)
        if existe:
            banco.id = existe.id
            return banco

        # creacion
        nuevo_banco = BancoORM(nombre=banco.nombre)
        self.db.add(nuevo_banco)
        self.db.flush()
        self.db.refresh(nuevo_banco)

        banco.id = nuevo_banco.id
        return banco

    def obtener(self, banco: Banco):
        existe = self.db.query(BancoORM).filter_by(nombre=banco.nombre).first()
        if existe:
            return existe
        else:
            return None
