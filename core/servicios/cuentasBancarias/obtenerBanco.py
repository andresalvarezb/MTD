from core.interfaces.repositorioBanco import ObtenerBancoPorNombreProtocol
from core.servicios.cuentasBancarias.dtos import ObtenerBancoDTO


class ObtenerBanco:
    def __init__(self, repo_obtener: ObtenerBancoPorNombreProtocol):
        self.repo_obtener = repo_obtener

    def ejecutar(self, data: ObtenerBancoDTO):
        banco = self.repo_obtener.obtener_por_nombre(data.nombre)
        if not banco:
            raise ValueError("Banco no encontrado")

        return banco
