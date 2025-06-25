from sqlalchemy.orm import Session
from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario
from infraestructura.db.modelos.historialLaboralUsuario import HistorialLaboralORM
from core.interfaces.repositorioHistorialLaboralUsuario import (
    CrearHistorialLaboralUsuarioProtocol,
    ObtenerHistorialLaboralPorIdProtocol,
    ActulizarSeguridadSocialHistorialLaboralProtocol,
    ObtenerHistorialLaboralPorClaveProtocol,
)


class RepositorioHistorialLaboralUsuarioSqlAlchemy(
    CrearHistorialLaboralUsuarioProtocol,
    ObtenerHistorialLaboralPorIdProtocol,
    ActulizarSeguridadSocialHistorialLaboralProtocol,
    ObtenerHistorialLaboralPorClaveProtocol,
):
    def __init__(self, db: Session):
        self.db = db

    # def guardar(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario:
    #     """Implementación para guardar un HistorialLaboralUsuario en la base de datos"""

    #     # verificar existencia
    #     existe = self.obtener(historialLaboral)
    #     if existe:
    #         historialLaboral.id = existe.id
    #         return historialLaboral

    #     # creacion
    #     nuevo_HistorialLaboralUsuario = HistorialLaboralORM(**historialLaboral.__dict__)
    #     self.db.add(nuevo_HistorialLaboralUsuario)
    #     self.db.flush()
    #     self.db.refresh(nuevo_HistorialLaboralUsuario)

    #     historialLaboral.id = nuevo_HistorialLaboralUsuario.id
    #     return historialLaboral

    def crear(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario:
        nuevo_historial = HistorialLaboralORM(**historialLaboral.__dict__)
        self.db.add(nuevo_historial)
        self.db.flush()
        self.db.refresh(nuevo_historial)
        historialLaboral.id = nuevo_historial.id
        return historialLaboral

    def obtener(self, historialLaboral: HistorialLaboralUsuario):
        existe = self.db.query(HistorialLaboralORM).filter_by(claveHLU=historialLaboral.claveHLU).first()
        if existe:
            return existe
        else:
            return None

    def actualizar_seguridad_social(self, historialLaboral: HistorialLaboralUsuario):
        registro_orm = self.obtener(historialLaboral)
        if not registro_orm:
            raise ValueError("Usuario no encontrado")
        registro_orm.seguridad_social = historialLaboral.seguridad_social
        return HistorialLaboralUsuario.from_orm(registro_orm)

    def obtener_por_id(self, id_historial_laboral: int) -> HistorialLaboralUsuario | None:
        registro_orm = self.db.query(HistorialLaboralORM).filter_by(id=id_historial_laboral).first()
        if not registro_orm:
            return None
        return HistorialLaboralUsuario.from_orm(registro_orm)

    def obtener_por_clave(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario | None:
        registro_orm = self.db.query(HistorialLaboralORM).filter_by(claveHLU=historialLaboral.claveHLU).first()
        if not registro_orm:
            return None
        return HistorialLaboralUsuario.from_orm(registro_orm)
