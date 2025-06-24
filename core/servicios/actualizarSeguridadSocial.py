from core.interfaces.repositorioUsuario import ObtenerUsuarioPorDocumentoProtocol, ActulizarSeguridadSocialUsuarioProtocol
from app.api.esquemas.seguridadSocial import ActualizacionSeguridadSocialSchema
from core.interfaces.repositorioHistorialLaboralUsuario import ObtenerHistorialLaboralPorIdProtocol, ActulizarSeguridadSocialHistorialLaboralProtocol


class ActualizarSeguridadSocial:
    def __init__(
        self,
        obtener_usuario_repo : ObtenerUsuarioPorDocumentoProtocol,
        obtener_hlu_repo : ObtenerHistorialLaboralPorIdProtocol,
        actualizar_ss_usuario_repo: ActulizarSeguridadSocialUsuarioProtocol,
        actualizar_ss_hlu_repo: ActulizarSeguridadSocialHistorialLaboralProtocol,
    ):
        self.obtener_usuario_repo = obtener_usuario_repo
        self.obtener_hlu_repo = obtener_hlu_repo
        self.actualizar_ss_usuario_repo = actualizar_ss_usuario_repo
        self.actualizar_ss_hlu_repo = actualizar_ss_hlu_repo


    def ejecutar(self, data: ActualizacionSeguridadSocialSchema):
        # obtener registros en base al id
        usuario = self.obtener_usuario_repo.obtener_por_documento(data.documento_usuario)
        if not usuario:
            raise ValueError(f"Usuario {data.documento_usuario} no encontrado")

        usuario.seguridad_social = data.tiene_seguridad_social
        usuario.fecha_aprobacion_seguridad_social = data.fecha_aprobacion_seguridad_social
        usuario = self.actualizar_ss_usuario_repo.actualizar_seguridad_social(usuario)

        historial_laboral = self.obtener_hlu_repo.obtener_por_id(data.id_cuenta_por_pagar)

        if not historial_laboral:
            raise ValueError(f"Historial laboral {data.id_cuenta_por_pagar} no encontrado")

        historial_laboral.seguridad_social = data.tiene_seguridad_social
        historial_laboral.fecha_aprobacion_seguridad_social = data.fecha_aprobacion_seguridad_social
        historial_laboral = self.actualizar_ss_hlu_repo.actualizar_seguridad_social(historial_laboral)
        return usuario, historial_laboral

        # actualizar seguridad social en ambas entidades

        # crear trigger que actualice el estado de requisto para pago
