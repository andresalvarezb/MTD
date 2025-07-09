from core.entidades.cuentaPorPagar import CuentaPorPagar
from core.interfaces.repositorioCuentaPorPagar import CrearCuentaPorPagarProtocol, ObtenerCuentaPorPagarPorClaveProtocol
from core.servicios.cuentasPorPagar.dtos import CrearCuentaPorPagarDTO


class CrearCuentaPorPagar:
    def __init__(self, repo_crear: CrearCuentaPorPagarProtocol, repo_obtener: ObtenerCuentaPorPagarPorClaveProtocol):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    def ejecutar(self, datos: CrearCuentaPorPagarDTO) -> CuentaPorPagar:
        cuenta = CuentaPorPagar(
            claveCPP=datos.claveCPP,
            historial_laboral=datos.historial_laboral,
            cuenta_bancaria=datos.cuenta_bancaria,
            fecha_prestacion_servicio=datos.fecha_prestacion_servicio,
            fecha_radicacion_contable=datos.fecha_radicacion_contable,
            estado_aprobacion_cuenta_usuario=datos.estado_aprobacion_cuenta_usuario,
            estado_cuenta_por_pagar=datos.estado_cuenta_por_pagar,
            valor_cuenta_cobro=datos.valor_cuenta_cobro,
            estado_de_pago=datos.estado_de_pago,
            # total_descuentos=datos.total_descuentos,
            # total_a_pagar=datos.total_a_pagar,
            fecha_actualizacion=datos.fecha_actualizacion,
            fecha_aprobacion_rut=datos.fecha_aprobacion_rut,
            fecha_creacion=datos.fecha_creacion,
            fecha_aprobacion_cuenta_usuario=datos.fecha_aprobacion_cuenta_usuario,
            fecha_programacion_pago=datos.fecha_programacion_pago,
            fecha_reprogramacion=datos.fecha_reprogramacion,
            fecha_pago=datos.fecha_pago,
            estado_reprogramacion_pago=datos.estado_reprogramacion_pago,
            rut=datos.rut,
            dse=datos.dse,
            causal_rechazo=datos.causal_rechazo,
            creado_por=datos.creado_por,
            lider_paciente_asignado=datos.lider_paciente_asignado,
            eps_paciente_asignado=datos.eps_paciente_asignado,
        )

        cuenta_existente = self.repo_obtener.obtener_por_clave(cuenta.claveCPP)
        if cuenta_existente:
            return cuenta_existente

        cuenta_nueva = self.repo_crear.crear(cuenta)
        return cuenta_nueva
