from core.interfaces.repositorioDeuda import ObtenerDeudasProtocol

class ObtenerDeudas:
    def __init__(self, repo_deuda: ObtenerDeudasProtocol):
        self.repo_deuda = repo_deuda

    def ejecutar(self):
        return self.repo_deuda.obtener_todas()