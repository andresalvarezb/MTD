from core.interfaces.repositorioMunicipio import ObtenerMunicipioPorNombreProtocol
from core.servicios.municipio.dtos import ObtenerMunicipioDTO
from core.entidades.municipio import Municipio


class ObtenerMunicipio:
    def __init__(self, repo_obtener: ObtenerMunicipioPorNombreProtocol):
        self.repo_obtener = repo_obtener

    def ejecutar(self, municipiodto: ObtenerMunicipioDTO):
        municipio = Municipio(nombre=municipiodto.nombre)
        municipio_obtenido = self.repo_obtener.obtener_por_nombre(municipio)
        if not municipio_obtenido:
            raise ValueError("Municipio no encontrado. Puede estar mal escrito o no creado")
        return municipio_obtenido
