from sqlalchemy.orm import Session
from core.entidades.areaMtd import AreaMTD
from infraestructura.db.modelos.areaMTD import AreaMTDORM
from core.interfaces.repositorioAreaMTD import ObtenerAreaPorNombreProtocol, CrearAreaMTDProtocol


class RepositorioAreaMTDSqlAlchemy(CrearAreaMTDProtocol, ObtenerAreaPorNombreProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(self, area: AreaMTD) -> AreaMTD:
        """Implementación para guardar el AreaMTD en la base de datos"""

        nueva_area = AreaMTDORM(nombre=area.nombre)
        self.db.add(nueva_area)
        self.db.flush()
        self.db.refresh(nueva_area)
        return AreaMTD.from_orm(nueva_area)

    def obtener_por_nombre(self, nombre_area: str) -> AreaMTD | None:
        registro_orm = self.db.query(AreaMTDORM).filter_by(nombre=nombre_area).first()
        if not registro_orm:
            return None
        return AreaMTD.from_orm(registro_orm)
