from sqlalchemy.orm import Session
from core.entidades.municipio import Municipio
from infraestructura.db.modelos.municipio import MunicipioORM
from core.interfaces.repositorioMunicipio import (
    CrearMunicipioProtocol,
    ObtenerMunicipioPorNombreProtocol,
    ObtenerMunicipioPorIdProtocol,
)


class RepositorioMunicipioSqlAlchemy(
    CrearMunicipioProtocol, ObtenerMunicipioPorNombreProtocol, ObtenerMunicipioPorIdProtocol
):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, municipio: Municipio) -> Municipio:
        if not municipio.departamento:
            raise ValueError("El municipio debe estar asociado a un departamento")

        nuevo_municipio = MunicipioORM(nombre=municipio.nombre, id_departamento=municipio.departamento.id)
        self.db.add(nuevo_municipio)
        self.db.flush()
        self.db.refresh(nuevo_municipio)
        return Municipio.from_orm(nuevo_municipio)

    def obtener_por_nombre(self, municipio: Municipio) -> Municipio | None:
        registro_orm = self.db.query(MunicipioORM).filter_by(nombre=municipio.nombre).first()
        if registro_orm:
            return Municipio.from_orm(registro_orm)
        else:
            return None

    def obtener_por_id(self, id_municipio: int) -> Municipio | None:
        registro_orm = self.db.query(MunicipioORM).filter_by(id=id_municipio).first()
        if registro_orm:
            return Municipio.from_orm(registro_orm)
        else:
            return None
