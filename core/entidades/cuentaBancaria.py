from dataclasses import dataclass
from datetime import datetime


@dataclass
class CuentaBancaria:
    numero_cuenta: str
    numero_certificado: str
    estado: str
    id_usuario: int
    id_banco: int
    id: int | None = None
    tipo_de_cuenta: str | None = None
    fecha_actualizacion: datetime | None = None
    observaciones: str | None = None

    def actualizar_cuenta(
        self,
        numero_cuenta: str | None,
        numero_certificado: str | None,
        tipo_de_cuenta: str | None,
        id_banco: int | None,
    ):
        # Actualizar y validar número de cuenta (si se pasa)
        if numero_cuenta is not None:
            if len(numero_cuenta) < 5:
                raise ValueError("El número de cuenta debe tener al menos 5 caracteres.")
            if not numero_cuenta.isdigit():
                raise ValueError("El número de cuenta debe contener solo dígitos.")
            self.numero_cuenta = numero_cuenta

        # Actualizar y validar número de certificado
        if numero_certificado is not None:
            if len(numero_certificado.strip()) == 0:
                raise ValueError("El número de certificado no puede estar vacío.")
            self.numero_certificado = numero_certificado

        # Actualizar y validar tipo de cuenta
        if tipo_de_cuenta is not None:
            tipos_validos = {"ahorros", "corriente", "nomina"}
            if tipo_de_cuenta.lower() not in tipos_validos:
                raise ValueError(f"Tipo de cuenta inválido. Debe ser uno de: {', '.join(tipos_validos)}")
            self.tipo_de_cuenta = tipo_de_cuenta.lower()

        # Actualizar y validar id_banco
        if id_banco is not None:
            if not isinstance(id_banco, int) or id_banco <= 0:
                raise ValueError("El ID del banco debe ser un número entero positivo.")
            self.id_banco = id_banco

        # Siempre se actualiza la fecha
        self.fecha_actualizacion = datetime.now()
