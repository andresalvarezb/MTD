from enum import Enum


class EnumEstadoUsuario(Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"

    @classmethod
    def tiene_valor(cls, valor: str) -> bool:
        return valor in cls._value2member_map_


class EnumTipoContrato(Enum):
    OPS = "OPS"
    NOMINA = "NOMINA"


class EnumEPS(Enum):
    NUEVA_EPS = "NUEVA EPS"
    SALUD_TOTAL = "SALUD TOTAL"
    SURA = "SURA"
    SANITAS = "SANITAS"
    COOMEVA = "COOMEVA"
    COMPENSAR = "COMPENSAR"
    COMFENALCO = "COMFENALCO"
    COOSALUD = "COOSALUD"


class EnumEstadoDePago(Enum):
    EXITOSO = "EXITOSO"
    PENDIENTE = "PENDIENTE"
    REPROGRAMADO = "REPROGRAMADO"


class EnumEstadoAprobacionUsuario(Enum):
    APROBADO = "ACEPTAR"
    RECHAZADO = "RECHAZAR"
    PENDIENTE = "PENDIENTE"


class EnumEstadoCuentaPorPagar(Enum):
    ACTIVA = "PROCEDE PARA PAGO"
    INACTIVA = "NO PROCEDE PARA PAGO"
