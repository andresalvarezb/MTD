from sqlalchemy.orm import Session
from core.entidades.municipio import Municipio, Departamento
from infraestructura.db.modelos.municipio import DepartamentoORM, MunicipioORM
from core.interfaces.repositorioMunicipio import CrearDepartamentoProtocol, ObtenerDepartamentoPorNombreProtocol, CrearMunicipioProtocol, ObtenerMunicipioPorNombreProtocol



class RepositorioDepartamentoSqlAlchemy(CrearDepartamentoProtocol, ObtenerDepartamentoPorNombreProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    # def guardar(self, departamento: Departamento) -> Departamento:
    #     """Implementación para guardar el departamento en la base de datos"""

    #     # verificar existencia
    #     existe = self.obtener(departamento)
    #     if existe:
    #         departamento.id = existe.id
    #         return departamento

    #     # creacion
    #     nuevo_departamento = DepartamentoORM(nombre=departamento.nombre)
    #     self.db.add(nuevo_departamento)
    #     self.db.flush()
    #     self.db.refresh(nuevo_departamento)

    #     departamento.id = nuevo_departamento.id
    #     return departamento

    def obtener_por_nombre(self, departamento: Departamento) -> Departamento | None:
        registro_orm = self.db.query(DepartamentoORM).filter_by(nombre=departamento.nombre).first()
        if registro_orm:
            return Departamento.from_orm(registro_orm)
        else:
            return None

    def crear(self, departamento: Departamento) -> Departamento:
        nuevo_departamento = DepartamentoORM(nombre=departamento.nombre)
        self.db.add(nuevo_departamento)
        self.db.flush()
        self.db.refresh(nuevo_departamento)
        departamento.id = nuevo_departamento.id
        return departamento





class RepositorioMunicipioSqlAlchemy(CrearMunicipioProtocol, ObtenerMunicipioPorNombreProtocol):
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
        nuevo_municipio = MunicipioORM(nombre=municipio.nombre)
        self.db.add(nuevo_municipio)
        self.db.flush()
        self.db.refresh(nuevo_municipio)
        municipio.id = nuevo_municipio.id
        return municipio
