from core.interfaces.repositorioAreaMTD import ObtenerAreasProtocol


class ObtenerAreasMTD:
    def __init__(self, repo_obtener: ObtenerAreasProtocol):
        self.repo_obtener = repo_obtener

    def ejecutar(self):
        return self.repo_obtener.obtener_todos()
