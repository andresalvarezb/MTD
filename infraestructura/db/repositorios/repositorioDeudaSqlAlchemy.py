from sqlalchemy.orm import Session
from core.entidades.deuda import Deuda
from infraestructura.db.modelos.deuda import DeudaORM
from core.interfaces.repositorioDeuda import CrearDeudaProtocol, ObtenerDeudasProtocol


class RepositorioDeudaSqlAlchemy(CrearDeudaProtocol, ObtenerDeudasProtocol):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, deuda: Deuda) -> Deuda:
        """Implementación para guardar un Deuda en la base de datos"""

        # verificar existencia
        existe = self.obtener(deuda)
        if existe:
            deuda.id = existe.id
            return deuda

        # creacion
        nuevo_deuda = DeudaORM(**deuda.__dict__)
        self.db.add(nuevo_deuda)
        self.db.flush()
        self.db.refresh(nuevo_deuda)

        deuda.id = nuevo_deuda.id
        return deuda

    def obtener(self, deuda: Deuda):
        existe = (
            self.db.query(DeudaORM).filter_by(id_usuario=deuda.id_usuario, fecha_creacion=deuda.fecha_creacion).first()
        )
        if existe:
            return existe
        else:
            return None

    def obtener_todas(self) -> list[Deuda]:
        deudas = self.db.query(DeudaORM).all()
        return [Deuda.from_orm(deuda) for deuda in deudas]