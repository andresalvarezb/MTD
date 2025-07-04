from core.interfaces.repositorioDeuda import EliminarDeudaProtocol


class EliminarDeuda:
    def __init__(self, repo_deuda: EliminarDeudaProtocol):
        self.repo_deuda = repo_deuda

    def ejecutar(self, id_deuda: int):
        if not id_deuda:
            raise ValueError(f"No hay identificardor para eliminar la deuda.")
        return self.repo_deuda.eliminar(id_deuda)
