from sqlalchemy.orm import Session
from core.entidades.municipio import Municipio, Departamento
from infraestructura.db.modelos.municipio import DepartamentoORM, MunicipioORM
from core.interfaces.repositorioMunicipio import (
    CrearDepartamentoProtocol,
    ObtenerDepartamentoPorNombreProtocol,
    CrearMunicipioProtocol,
    ObtenerMunicipioPorNombreProtocol,
    ObtenerDepartamentoPorIdProtocol,
    ObtenerMunicipioPorIdProtocol,
)


class RepositorioDepartamentoSqlAlchemy(
    CrearDepartamentoProtocol, ObtenerDepartamentoPorNombreProtocol, ObtenerDepartamentoPorIdProtocol
):
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(self, departamento: Departamento) -> Departamento:
        nuevo_departamento = DepartamentoORM(nombre=departamento.nombre)
        self.db.add(nuevo_departamento)
        self.db.flush()
        self.db.refresh(nuevo_departamento)
        # departamento.id = nuevo_departamento.id
        # return departamento
        return Departamento.from_orm(nuevo_departamento)

    def obtener_por_nombre(self, departamento: Departamento) -> Departamento | None:
        registro_orm = self.db.query(DepartamentoORM).filter_by(nombre=departamento.nombre).first()
        if registro_orm:
            return Departamento.from_orm(registro_orm)
        else:
            return None

    def obtener_por_id(self, id_departamento: int) -> Departamento | None:
        registro_orm = self.db.query(DepartamentoORM).filter_by(id=id_departamento).first()
        if registro_orm:
            return Departamento.from_orm(registro_orm)
        else:
            return None


class RepositorioMunicipioSqlAlchemy(
    CrearMunicipioProtocol, ObtenerMunicipioPorNombreProtocol, ObtenerMunicipioPorIdProtocol
):
    def __init__(self, db: Session):
        self.db = db

    # def guardar(self, municipio: Municipio) -> Municipio:
    #     "Implementación para guardar el municipio en la base de datos"

    #     # verificar existencia
    #     existe = self.obtener(municipio)
    #     if existe:
    #         municipio.id = existe.id
    #         return municipio

    #     # creacion
    #     nuevo_municipio = MunicipioORM(nombre=municipio.nombre, id_departamento=municipio.id_departamento)
    #     self.db.add(nuevo_municipio)
    #     self.db.flush()
    #     self.db.refresh(nuevo_municipio)

    #     municipio.id = nuevo_municipio.id
    #     return municipio

    def obtener_por_nombre(self, municipio: Municipio) -> Municipio | None:
        registro_orm = self.db.query(MunicipioORM).filter_by(nombre=municipio.nombre).first()
        if registro_orm:
            return Municipio.from_orm(registro_orm)
        else:
            return None

    def crear(self, municipio: Municipio) -> Municipio:
        nuevo_municipio = MunicipioORM(nombre=municipio.nombre, id_departamento=municipio.id_departamento)
        self.db.add(nuevo_municipio)
        self.db.flush()
        self.db.refresh(nuevo_municipio)
        municipio.id = nuevo_municipio.id
        return municipio

    def obtener_por_id(self, id_municipio: int) -> Municipio | None:
        registro_orm = self.db.query(MunicipioORM).filter_by(id=id_municipio).first()
        if registro_orm:
            return Municipio.from_orm(registro_orm)
        else:
            return None
