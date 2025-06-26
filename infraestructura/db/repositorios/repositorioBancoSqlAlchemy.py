from sqlalchemy.orm import Session
from core.entidades.banco import Banco
from infraestructura.db.modelos.banco import BancoORM
from core.interfaces.repositorioBanco import CrearBancoProtocol, ObtenerBancoPorNombreProtocol


class RepositorioBancoSqlAlchemy(CrearBancoProtocol, ObtenerBancoPorNombreProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(self, banco: Banco) -> Banco:
        banco_nuevo = BancoORM(nombre=banco.nombre)
        self.db.add(banco_nuevo)
        self.db.flush()
        self.db.refresh(banco_nuevo)
        banco.id = banco_nuevo.id
        return banco

    def obtener_por_nombre(self, nombre: str) -> Banco | None:
        registro_orm = self.db.query(BancoORM).filter_by(nombre=nombre).first()
        if registro_orm:
            return Banco.from_orm(registro_orm)
        else:
            return None
