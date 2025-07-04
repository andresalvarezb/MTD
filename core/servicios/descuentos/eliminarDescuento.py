from core.interfaces.repositorioDescuento import EliminarDescuentoProtocol


class EliminarDescuento:
    def __init__(self, repo_eliminar: EliminarDescuentoProtocol):
        self.repo_eliminar = repo_eliminar

    def ejecutar(self, id_descuento: int) -> None:
        self.repo_eliminar.eliminar(id_descuento)
        return None
