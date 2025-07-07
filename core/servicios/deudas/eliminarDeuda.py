from core.interfaces.repositorioDeuda import EliminarDeudaProtocol


class EliminarDeuda:
    def __init__(self, repo_deuda: EliminarDeudaProtocol):
        self.repo_deuda = repo_deuda

    def ejecutar(self, id_deuda: int):
        return self.repo_deuda.eliminar(id_deuda)
