from sqlalchemy.orm import Session
from core.entidades.areaMtd import AreaMTD
from infraestructura.db.modelos.areaMTD import AreaMTDORM
from core.interfaces.repositorioAreaMTD import ObtenerAreaPorNombreProtocol


class RepositorioAreaMTDSqlAlchemy(ObtenerAreaPorNombreProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def guardar(self, area: AreaMTD) -> AreaMTD:
        """Implementación para guardar el AreaMTD en la base de datos"""

        # verificar existencia
        registro_orm = self.db.query(AreaMTDORM).filter_by(nombre=area.nombre).first()
        if registro_orm:
            area.id = registro_orm.id
            return area

        # creacion
        nueva_area = AreaMTDORM(nombre=area.nombre)
        self.db.add(nueva_area)
        self.db.flush()
        self.db.refresh(nueva_area)

        area.id = nueva_area.id
        return area

    def obtener_por_nombre(self, nombre_area: str) -> AreaMTD | None:
        registro_orm = self.db.query(AreaMTDORM).filter_by(nombre=nombre_area).first()
        if not registro_orm:
            return None
        return AreaMTD.from_orm(registro_orm)
