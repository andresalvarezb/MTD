from app.api.esquemas.cuentaPorPagar import CuentaPorPagarResponseSchema
from core.interfaces.repositorioCuentaPorPagar import ObtenerCuentaPorPagarPorIdProtocol


class ObtenerCuentaPorPagar:
    def __init__(self, repositorio: ObtenerCuentaPorPagarPorIdProtocol):
        self.repositorio = repositorio

    def ejecutar(self, id_cuenta_por_pagar: int):
        cuenta = self.repositorio.obtener_por_id(id_cuenta_por_pagar)
        if not cuenta:
            raise Exception("cuenta no encontrada")
    
        cuenta_bancaria_schema = {
            "id": cuenta.cuenta_bancaria.id,
            "id_usuario": cuenta.cuenta_bancaria.usuario.id,
            "numero_cuenta": cuenta.cuenta_bancaria.numero_cuenta,
            "numero_certificado": cuenta.cuenta_bancaria.numero_certificado,
            "estado": cuenta.cuenta_bancaria.estado,
            "tipo_de_cuenta": cuenta.cuenta_bancaria.tipo_de_cuenta,
            "fecha_actualizacion": cuenta.cuenta_bancaria.fecha_actualizacion,
            "observaciones": cuenta.cuenta_bancaria.observaciones,
            "banco": cuenta.cuenta_bancaria.banco,
        }
        return CuentaPorPagarResponseSchema(
            id=cuenta.id,
            claveCPP=cuenta.claveCPP,
            fecha_prestacion_servicio=cuenta.fecha_prestacion_servicio,
            fecha_radicacion_contable=cuenta.fecha_radicacion_contable,
            estado_de_pago=cuenta.estado_de_pago,
            estado_aprobacion_cuenta_usuario=cuenta.estado_aprobacion_cuenta_usuario,
            estado_cuenta_por_pagar=cuenta.estado_cuenta_por_pagar,
            valor_cuenta_cobro=cuenta.valor_cuenta_cobro,
            total_descuentos=cuenta.total_descuentos,
            total_a_pagar=cuenta.total_a_pagar,
            fecha_actualizacion=cuenta.fecha_actualizacion,
            fecha_aprobacion_rut=cuenta.fecha_aprobacion_rut,
            fecha_creacion=cuenta.fecha_creacion,
            fecha_aprobacion_cuenta_usuario=cuenta.fecha_aprobacion_cuenta_usuario,
            fecha_programacion_pago=cuenta.fecha_programacion_pago,
            fecha_reprogramacion=cuenta.fecha_reprogramacion,
            fecha_pago=cuenta.fecha_pago,
            estado_reprogramacion_pago=cuenta.estado_reprogramacion_pago,
            rut=cuenta.rut,
            dse=cuenta.dse,
            causal_rechazo=cuenta.causal_rechazo,
            creado_por=cuenta.creado_por,
            lider_paciente_asignado=cuenta.lider_paciente_asignado,
            eps_paciente_asignado=cuenta.eps_paciente_asignado,
            historial_laboral=cuenta.historial_laboral,
            cuenta_bancaria=cuenta_bancaria_schema,
        )