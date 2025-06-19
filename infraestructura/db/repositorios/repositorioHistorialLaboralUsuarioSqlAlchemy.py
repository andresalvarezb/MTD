from sqlalchemy.orm import Session
from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario
from infraestructura.db.modelos.historialLaboralUsuario import HistorialLaboralORM
from core.interfaces.repositorioHistorialLaboralUsuario import RepositorioHistorialLaboralUsuario


class RepositorioHistorialLaboralUsuarioSqlAlchemy(RepositorioHistorialLaboralUsuario):
    def __init__(self, db: Session):
        self.db = db

    def guardar(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario:
        """Implementación para guardar un HistorialLaboralUsuario en la base de datos"""

        # verificar existencia
        existe = self.obtener(historialLaboral)
        if existe:
            historialLaboral.id = existe.id
            return historialLaboral

        # creacion
        nuevo_HistorialLaboralUsuario = HistorialLaboralORM(**historialLaboral.__dict__)
        self.db.add(nuevo_HistorialLaboralUsuario)
        self.db.flush()
        self.db.refresh(nuevo_HistorialLaboralUsuario)

        historialLaboral.id = nuevo_HistorialLaboralUsuario.id
        return historialLaboral

    def obtener(self, historialLaboral: HistorialLaboralUsuario):
        existe = self.db.query(HistorialLaboralORM).filter_by(claveHLU=historialLaboral.claveHLU).first()
        if existe:
            return existe
        else:
            return None
