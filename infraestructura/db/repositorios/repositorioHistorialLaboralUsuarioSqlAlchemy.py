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

    def crear(self, historialLaboral: HistorialLaboralUsuario) -> HistorialLaboralUsuario:
        nuevo_historial = HistorialLaboralORM(
            id_municipio=historialLaboral.municipio.id,
            contrato=historialLaboral.contrato,
            id_cargo=historialLaboral.cargo.id,
            fecha_contratacion=historialLaboral.fecha_contratacion,
            claveHLU=historialLaboral.claveHLU,
            seguridad_social=historialLaboral.seguridad_social,
            fecha_aprobacion_seguridad_social=historialLaboral.fecha_aprobacion_seguridad_social,
            fecha_ultima_contratacion=historialLaboral.fecha_ultima_contratacion,
            fecha_fin_contratacion=historialLaboral.fecha_fin_contratacion,
            id_usuario=historialLaboral.usuario.id,
        )
        self.db.add(nuevo_historial)
        self.db.flush()
        self.db.refresh(nuevo_historial)
        return historialLaboral.from_orm(nuevo_historial)

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
