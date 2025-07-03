from sqlalchemy.orm import Session
from datetime import datetime
from core.entidades.cuentaPorPagar import CuentaPorPagar
from infraestructura.db.modelos.cuentaPorPagar import CuentaPorPagarORM
from core.interfaces.repositorioCuentaPorPagar import (
    CrearCuentaPorPagarProtocol,
    ObtenerCuentaPorPagarProtocol,
    ObtenerCuentasPorPagarProtocol,
    ObtenerCuentaPorPagarPorClaveProtocol,
    ObtenerCuentaPorPagarPorIdProtocol,
    ActualizarCuentaPorPagarProtocol,
)
from fastapi import HTTPException
from infraestructura.db.modelos.historialLaboralUsuario import HistorialLaboralORM
from infraestructura.db.modelos.usuario import UsuarioORM
from infraestructura.db.modelos.municipio import MunicipioORM

# from infraestructura.db.modelos.cargo import CargoORM
from sqlalchemy.orm import joinedload
from infraestructura.db.modelos.cuentaBancaria import CuentaBancariaORM


class RepositorioCuentaPorPagarSqlAlchemy(
    CrearCuentaPorPagarProtocol,
    ObtenerCuentaPorPagarProtocol,
    ObtenerCuentasPorPagarProtocol,
    ObtenerCuentaPorPagarPorClaveProtocol,
    ObtenerCuentaPorPagarPorIdProtocol,
    ActualizarCuentaPorPagarProtocol,
):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, cuenta_por_pagar: CuentaPorPagar) -> CuentaPorPagar:
        cuenta_nueva = CuentaPorPagarORM(
            claveCPP=cuenta_por_pagar.claveCPP,
            id_historial_laboral=cuenta_por_pagar.historial_laboral.id,
            id_cuenta_bancaria=cuenta_por_pagar.cuenta_bancaria.id,
            fecha_prestacion_servicio=cuenta_por_pagar.fecha_prestacion_servicio,
            fecha_radicacion_contable=cuenta_por_pagar.fecha_radicacion_contable,
            estado_aprobacion_cuenta_usuario=cuenta_por_pagar.estado_aprobacion_cuenta_usuario,
            estado_cuenta_por_pagar=cuenta_por_pagar.estado_cuenta_por_pagar,
            valor_cuenta_cobro=cuenta_por_pagar.valor_cuenta_cobro,
            total_descuentos=cuenta_por_pagar.total_descuentos,
            total_a_pagar=cuenta_por_pagar.total_a_pagar,
            fecha_actualizacion=datetime.now(),
            fecha_aprobacion_rut=cuenta_por_pagar.fecha_aprobacion_rut,
            fecha_creacion=datetime.now(),
            fecha_aprobacion_cuenta_usuario=cuenta_por_pagar.fecha_aprobacion_cuenta_usuario,
            fecha_programacion_pago=cuenta_por_pagar.fecha_programacion_pago,
            fecha_reprogramacion=cuenta_por_pagar.fecha_reprogramacion,
            fecha_pago=cuenta_por_pagar.fecha_pago,
            estado_reprogramacion_pago=cuenta_por_pagar.estado_reprogramacion_pago,
            rut=cuenta_por_pagar.rut,
            dse=cuenta_por_pagar.dse,
            causal_rechazo=cuenta_por_pagar.causal_rechazo,
            creado_por=cuenta_por_pagar.creado_por,
            lider_paciente_asignado=cuenta_por_pagar.lider_paciente_asignado,
            eps_paciente_asignado=cuenta_por_pagar.eps_paciente_asignado,
        )
        self.db.add(cuenta_nueva)
        self.db.commit()
        self.db.refresh(cuenta_nueva)
        return cuenta_por_pagar.from_orm(cuenta_nueva)

    def obtener(self, cuenta_por_pagar: CuentaPorPagar):
        existe = self.db.query(CuentaPorPagarORM).filter_by(claveCPP=cuenta_por_pagar.claveCPP).first()
        if existe:
            return existe
        else:
            return None

    def actualizar(self, cuenta_por_pagar: CuentaPorPagar):
        registro_orm = self.db.query(CuentaPorPagarORM).filter_by(id=cuenta_por_pagar.id).first()

        if not registro_orm:
            raise ValueError("Cuenta por pagar no encontrado")

        if not cuenta_por_pagar.historial_laboral.id:
            raise ValueError("Historial laboral no asociado")

        if not cuenta_por_pagar.cuenta_bancaria.id:
            raise ValueError("cuenta bancaria no asociada")

        registro_orm.id_historial_laboral = cuenta_por_pagar.historial_laboral.id
        registro_orm.id_cuenta_bancaria = cuenta_por_pagar.cuenta_bancaria.id
        registro_orm.fecha_prestacion_servicio = cuenta_por_pagar.fecha_prestacion_servicio
        registro_orm.fecha_radicacion_contable = cuenta_por_pagar.fecha_radicacion_contable
        registro_orm.estado_aprobacion_cuenta_usuario = cuenta_por_pagar.estado_aprobacion_cuenta_usuario
        registro_orm.estado_cuenta_por_pagar = cuenta_por_pagar.estado_cuenta_por_pagar
        registro_orm.valor_cuenta_cobro = cuenta_por_pagar.valor_cuenta_cobro  # type: ignore
        registro_orm.total_descuentos = cuenta_por_pagar.total_descuentos  # type: ignore
        registro_orm.total_a_pagar = cuenta_por_pagar.total_a_pagar  # type: ignore
        registro_orm.fecha_actualizacion = datetime.now()
        registro_orm.fecha_aprobacion_rut = cuenta_por_pagar.fecha_aprobacion_rut
        registro_orm.fecha_creacion = cuenta_por_pagar.fecha_creacion
        registro_orm.fecha_aprobacion_cuenta_usuario = cuenta_por_pagar.fecha_aprobacion_cuenta_usuario
        registro_orm.fecha_programacion_pago = cuenta_por_pagar.fecha_programacion_pago
        registro_orm.fecha_reprogramacion = cuenta_por_pagar.fecha_reprogramacion
        registro_orm.fecha_pago = cuenta_por_pagar.fecha_pago
        registro_orm.estado_reprogramacion_pago = cuenta_por_pagar.estado_reprogramacion_pago
        registro_orm.rut = cuenta_por_pagar.rut  # type: ignore
        registro_orm.dse = cuenta_por_pagar.dse
        registro_orm.causal_rechazo = cuenta_por_pagar.causal_rechazo

        self.db.flush()
        return CuentaPorPagar.from_orm(registro_orm)

    def obtener_cuentas_por_pagar(self) -> list[CuentaPorPagar]:
        registros_orm = (
            self.db.query(CuentaPorPagarORM)
            .options(
                joinedload(CuentaPorPagarORM.historial_laboral)
                .joinedload(HistorialLaboralORM.usuario)
                .joinedload(UsuarioORM.cargo),
                joinedload(CuentaPorPagarORM.historial_laboral)
                .joinedload(HistorialLaboralORM.usuario)
                .joinedload(UsuarioORM.municipio)
                .joinedload(MunicipioORM.departamento),
                joinedload(CuentaPorPagarORM.historial_laboral).joinedload(HistorialLaboralORM.cargo),
                joinedload(CuentaPorPagarORM.cuenta_bancaria).joinedload(CuentaBancariaORM.banco),
            )
            .all()
        )
        return [CuentaPorPagar.from_orm(orm_obj) for orm_obj in registros_orm]

    def obtener_cuenta_por_pagar(self, id_cuenta_por_pagar: int) -> CuentaPorPagar:
        registro = self.db.query(CuentaPorPagarORM).filter_by(id=id_cuenta_por_pagar).first()
        if not registro:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return CuentaPorPagar.from_orm(registro)

    def obtener_por_clave(self, clave: str) -> CuentaPorPagar | None:
        registro = self.db.query(CuentaPorPagarORM).filter_by(claveCPP=clave).first()
        if not registro:
            return None
        return CuentaPorPagar.from_orm(registro)

    # def obtener_por_id(self, id_cuenta_por_pagar: int) -> CuentaPorPagar | None:
    #     registro_orm = (
    #         self.db.query(CuentaPorPagarORM)
    #         .options(
    #             joinedload(CuentaPorPagarORM.historial_laboral)
    #             .joinedload(HistorialLaboralORM.usuario)
    #             .joinedload(UsuarioORM.cargo),
    #             joinedload(CuentaPorPagarORM.historial_laboral)
    #             .joinedload(HistorialLaboralORM.usuario)
    #             .joinedload(UsuarioORM.municipio)
    #             .joinedload(MunicipioORM.departamento),
    #             joinedload(CuentaPorPagarORM.historial_laboral).joinedload(HistorialLaboralORM.cargo),
    #             joinedload(CuentaPorPagarORM.cuenta_bancaria).joinedload(CuentaBancariaORM.banco),
    #         ).filter(CuentaPorPagarORM.id==id_cuenta_por_pagar)
    #         .first()
    #     )

    #     if not registro_orm:
    #         return None
    #     return CuentaPorPagar.from_orm(registro_orm)
    def obtener_por_id(self, id_cuenta_por_pagar: int) -> CuentaPorPagar | None:
        registro_orm = self.db.query(CuentaPorPagarORM).filter(CuentaPorPagarORM.id == id_cuenta_por_pagar).first()

        if not registro_orm:
            return None
        return CuentaPorPagar.from_orm(registro_orm)
