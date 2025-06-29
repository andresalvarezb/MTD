from core.entidades.banco import Banco
from core.servicios.cuentasBancarias.dtos import CrearBancoDTO
from core.interfaces.repositorioBanco import CrearBancoProtocol, ObtenerBancoPorNombreProtocol


class CrearBanco:
    def __init__(self, repo_crear: CrearBancoProtocol, repo_obtener: ObtenerBancoPorNombreProtocol):
        self.repo_crear = repo_crear
        self.repo_obtener = repo_obtener

    def ejecutar(self, datos: CrearBancoDTO) -> Banco:
        banco = Banco(nombre=datos.nombre)

        banco_existente = self.repo_obtener.obtener_por_nombre(banco.nombre)
        if banco_existente:
            return banco_existente

        banco = self.repo_crear.crear(banco)
        return banco
