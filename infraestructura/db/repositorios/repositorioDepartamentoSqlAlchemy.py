from sqlalchemy.orm import Session
from core.entidades.departamento import Departamento
from infraestructura.db.modelos.departamento import DepartamentoORM
from core.interfaces.repositorioDepartamento import (
    CrearDepartamentoProtocol,
    ObtenerDepartamentoPorNombreProtocol,
    ObtenerDepartamentoPorIdProtocol,
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
