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
            usuario=datos.usuario,
            contrato=datos.contrato,
            cargo=datos.cargo,
            municipio=datos.municipio,
            claveHLU=datos.claveHLU,
            fecha_contratacion=datos.fecha_contratacion,
            seguridad_social=datos.seguridad_social,
            fecha_aprobacion_seguridad_social=datos.fecha_aprobacion_seguridad_social,
            fecha_ultima_contratacion=datos.fecha_ultima_contratacion,
            fecha_fin_contratacion=datos.fecha_fin_contratacion,
        )

        historial_existente = self.repo_obtener.obtener_por_clave(historial)
        if historial_existente:
            return historial_existente

        # crear
        nuevo_historial = self.repo_crear.crear(historial)

        return nuevo_historial
