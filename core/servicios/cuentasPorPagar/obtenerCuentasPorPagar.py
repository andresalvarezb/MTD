from core.interfaces.repositorioCuentaPorPagar import ObtenerCuentasPorPagarProtocol
from core.interfaces.repositorioHistorialLaboralUsuario import ObtenerHistorialLaboralPorIdProtocol
from core.interfaces.repositorioCuentaBancaria import ObtenerCuentaBancariaPorIdProtocol
from app.api.esquemas.cuentaPorPagar import CuentaPorPagarCompletoResponseSchema
from core.interfaces.repositorioUsuario import ObtenerUsuarioPorIdProtocol
from core.interfaces.repositorioMunicipio import ObtenerMunicipioPorIdProtocol, ObtenerDepartamentoPorIdProtocol





# class ObtenerCuentasPorPagar:
#     def __init__(self, repositorio: ObtenerCuentasPorPagarProtocol):
#         self.repositorio = repositorio

#     def ejecutar(self):
#         return self.repositorio.obtener_cuentas_por_pagar()


class ObtenerCuentasPorPagar:
    def __init__(
        self,
        repo_cuenta_por_pagar: ObtenerCuentasPorPagarProtocol,
        repo_historial: ObtenerHistorialLaboralPorIdProtocol,
        repo_cuenta_bancaria: ObtenerCuentaBancariaPorIdProtocol,
        repo_usuario: ObtenerUsuarioPorIdProtocol,
        rerpo_municipio: ObtenerMunicipioPorIdProtocol,
        repo_departamento: ObtenerDepartamentoPorIdProtocol,
    ):
        self.repo_cuenta_por_pagar = repo_cuenta_por_pagar
        self.repo_historial = repo_historial
        self.repo_cuenta_bancaria = repo_cuenta_bancaria
        self.repo_usuario = repo_usuario
        self.repo_municipio = rerpo_municipio
        self.repo_departamento = repo_departamento



    def ejecutar(self):
        resultado = []
        cuentas = self.repo_cuenta_por_pagar.obtener_cuentas_por_pagar()

        for cuenta in cuentas:
            historial = self.repo_historial.obtener_por_id(cuenta.id_historial_laboral)
            if not historial:
                raise Exception("Cuanta por pagasr sin historial laboral asociado")
            cuenta_bancaria = self.repo_cuenta_bancaria.obtener_por_id(cuenta.id_cuenta_bancaria)

            if not cuenta_bancaria:
                raise Exception("Cuanta por pagar sin cuenta bancaria asociada")

            usuario = self.repo_usuario.obtener_por_id(historial.id_usuario)

            if not usuario:
                raise Exception("Cuanta por pagar sin usuario asociado")

            municipio = self.repo_municipio.obtener_por_id(usuario.id_municipio)

            if not municipio:
                raise Exception("Cuanta por pagar sin municipio asociado")

            departamento = self.repo_departamento.obtener_por_id(municipio.id_departamento)

            if not departamento:
                raise Exception("Cuanta por pagar sin departamento asociado")

            resultado.append(
                CuentaPorPagarCompletoResponseSchema(
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
                    tipo_de_cuenta=cuenta.tipo_de_cuenta,
                    usuario=usuario,
                    municipio=municipio,
                    departamento=departamento,
                    historial_laboral=historial,
                    cuenta_bancaria=cuenta_bancaria,
                )
            )
        return resultado