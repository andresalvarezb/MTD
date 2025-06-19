from datetime import datetime
from decimal import Decimal
from core.interfaces.repositorioCuentaPorPagar import RepositorioCuentaPorPagar
from core.entidades.cuentaPorPagar import CuentaPorPagar


class CrearCuentaPorPagar:
    def __init__(self, repositorio: RepositorioCuentaPorPagar):
        self.repositorio = repositorio

    def ejecutar(self, datos: dict) -> CuentaPorPagar:
        # 1. Crear la entidad desde los datos
        cuenta = CuentaPorPagar(
            id_historial_laboral=datos["id_historial_laboral"],
            id_cuenta_bancaria=datos["id_cuenta_bancaria"],
            claveCPP=datos["claveCPP"],
            fecha_prestacion_servicio=datos["fecha_prestacion_servicio"],
            fecha_radicacion_contable=datos["fecha_radicacion_contable"],
            estado_de_pago=datos["estado_de_pago"],
            estado_aprobacion_cuenta_usuario=datos["estado_aprobacion_cuenta_usuario"],
            estado_cuenta_por_pagar=datos["estado_cuenta_por_pagar"],
            valor_cuenta_cobro=datos["valor_cuenta_cobro"],
            total_a_pagar=datos["total_a_pagar"],
            fecha_actualizacion=datos["fecha_actualizacion"],
            fecha_aprobacion_rut=datos["fecha_aprobacion_rut"],
            fecha_creacion=datos["fecha_creacion"],
            fecha_aprobacion_cuenta_usuario=datos["fecha_aprobacion_cuenta_usuario"],
            fecha_programacion_pago=datos["fecha_programacion_pago"],
            fecha_reprogramacion=datos["fecha_reprogramacion"],
            fecha_pago=datos["fecha_pago"],
            estado_reprogramacion_pago=datos["estado_reprogramacion_pago"],
            rut=datos["rut"],
            dse=datos["dse"],
            causal_rechazo=datos["causal_rechazo"],
            creado_por=datos["creado_por"],
            lider_paciente_asignado=datos["lider_paciente_asignado"],
            eps_paciente_asignado=datos["eps_paciente_asignado"],
            tipo_de_cuenta=datos["tipo_de_cuenta"],
        )

        # 2. Guardar usando el repositorio
        self.repositorio.guardar(cuenta)

        return cuenta
