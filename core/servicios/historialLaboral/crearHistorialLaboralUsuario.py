from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario
from core.interfaces.repositorioHistorialLaboralUsuario import (
    CrearHistorialLaboralUsuarioProtocol,
    ObtenerHistorialLaboralPorClaveProtocol,
)
from core.servicios.historialLaboral.dtos import CrearHistorialLaboralUsuarioDTO


class CrearHistorialLaboralUsuario:
    def __init__(
        self, repo_crear: CrearHistorialLaboralUsuarioProtocol, repo_obtener: ObtenerHistorialLaboralPorClaveProtocol
    ):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    def ejecutar(self, datos: CrearHistorialLaboralUsuarioDTO) -> HistorialLaboralUsuario:
        # obtener
        historial = HistorialLaboralUsuario(
            id_municipio=datos.id_municipio,
            contrato=datos.contrato,
            id_cargo=datos.id_cargo,
            fecha_contratacion=datos.fecha_contratacion,
            claveHLU=datos.claveHLU,
            seguridad_social=datos.seguridad_social,
            fecha_aprobacion_seguridad_social=datos.fecha_aprobacion_seguridad_social,
            fecha_ultima_contratacion=datos.fecha_ultima_contratacion,
            fecha_fin_contratacion=datos.fecha_fin_contratacion,
            id_usuario=datos.id_usuario,
        )

        historial_existente = self.repo_obtener.obtener_por_clave(historial)
        if historial_existente:
            return historial_existente

        # crear
        nuevo_historial = self.repo_crear.crear(historial)

        return nuevo_historial
