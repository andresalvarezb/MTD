from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario
from core.interfaces.repositorioHistorialLaboralUsuario import CrearHistorialLaboralUsuarioProtocol


class CrearHistorialLaboralUsuario:
    def __init__(self, repositorio: CrearHistorialLaboralUsuarioProtocol):
        self.repositorio = repositorio

    def ejecutar(self, datos: dict) -> HistorialLaboralUsuario:

        historial = HistorialLaboralUsuario(
            id_municipio=datos["id_municipio"],
            contrato=datos["contrato"],
            id_cargo=datos["id_cargo"],
            fecha_contratacion=datos["fecha_contratacion"],
            claveHLU=datos["claveHLU"],
            seguridad_social=datos["seguridad_social"],
            fecha_aprobacion_seguridad_social=datos["fecha_aprobacion_seguridad_social"],
            fecha_ultima_contratacion=datos["fecha_ultima_contratacion"],
            fecha_fin_contratacion=datos["fecha_fin_contratacion"],
            id_usuario=datos["id_usuario"],
        )

        historial = self.repositorio.guardar(historial)

        return historial
