import pandas as pd
import numpy as np
from io import BytesIO
from fastapi import UploadFile, HTTPException
from datetime import datetime


MESES = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12",
}

RENOMBRAR_COLUMNAS = {
    "CARGO CONTRATISTA": "CARGO",
    "OPS O NOMINA": "TIPO_DE_CONTRATO",
    "ESTADO CONTRATISTA": "ESTADO_USUARIO",
    "TELEFONO DE CONTACTO": "TELEFONO_USUARIO",
    "NO.CUENTA BANCARIA": "NUM_CUENTA_BANCARIA",
    "NÚMERO DE DOCUMENTO CERTIFICADO BANCARIO": "NUM_CERTIFICADO_BANCARIO",
    "EPS PACIENTE ASIGNADO": "EPS_PACIENTE_ASIGNADO",
    "LIDER ASIGNADO": "LIDER_ASIGNADO_PACIENTE",
    "MES DE RADICACIÓN CONTABLE": "FECHA_RADICACION_CONTABLE",
    "FECHA DE SERVICIO": "FECHA_PRESTACION_SERVICIO",
    "VALOR CUENTA DE COBRO AUTOMATICA": "VALOR_CUENTA_DE_COBRO",
    "DESCUENTO RETEFUENTE": "DESCUENTO_RETEFUENTE",
    "DESCUENTO TESORERIA": "DESCUENTO_TESORERIA",
    "DESCUENTOS VARIOS": "DESCUENTOS_VARIOS",
    "VALOR DCTO S.S.": "DESCUENTO_SEGURIDAD_SOCIAL",
    "TOTAL A PAGAR": "TOTAL_A_PAGAR",
    "ESTADO CUENTA DE COBRO": "ESTADO_APROBACION_CUENTA_DE_COBRO",  # Aceptacion por parte del OPS
    "FECHA APROBACIÓN CUENTA DE COBRO": "FECHA_APROBACION_CUENTA_DE_COBRO",
    "SEGURIDAD SOCIAL": "ESTADO_SEGURIDAD_SOCIAL",
    "FECHA APROBACIÓN SEGURIDAD SOCIAL": "FECHA_APROBACION_SEGURIDAD_SOCIAL",
    "FECHA APROBACIÓN RUT": "FECHA_APROBACION_RUT",
    "FECHA OK CONTRATO": "FECHA_CONTRATACION",
    "ESTADO REQUISITOS PARA PAGO": "ESTADO_REQUISITOS_PARA_PAGO",
    "FECHA PROGRAMACION": "FECHA_PROGRAMACION_PAGO",
    "FECHA DE PAGO": "FECHA_PAGO",
    "ESTADO DE PAGO": "ESTADO_DE_PAGO",
    "CAUSAL DE RECHAZO": "CAUSAL_DE_RECHAZO",
    "FECHA REPROGRAMACIÓN PAGO": "FECHA_REPROGRAMACION_PAGO",
    "ESTADO DE REPROGRAMACIÓN": "ESTADO_DE_REPROGRAMACION",
    "VALOR MINIMO": "SALARIO_MINIMO_VIGENTE",
    "DESCUENTO REALIZADO": "OBSERVACION_DESCUENTO_ACTIVOS_FIJOS",
    "CANTIDAD DE DESCUENTOS": "NUMERO_DE_CUOTAS_A_DESCONTAR_ACTIVOS_FIJOS",
    "ACTIVO FIJO O DESCUENTO": "DESCRIPCION_DESCUENTO_ACTIVOS_FIJOS",
    "VALOR DESCUENTO": "VALOR_DESCUENTO_ACTIVOS_FIJOS",
}

tipo_columnas = {
    "DOCUMENTO": str,
    "TELEFONO_USUARIO": str,
    "NUM_CUENTA_BANCARIA": str,
    "NUM_CERTIFICADO_BANCARIO": str,
    "FECHA_CONTRATACION": "datetime64[ns]",
    "FECHA_APROBACION_SEGURIDAD_SOCIAL": "datetime64[ns]",
    "FECHA_RADICACION_CONTABLE": "datetime64[ns]",
    "FECHA_PRESTACION_SERVICIO": "datetime64[ns]",
    "FECHA_APROBACION_CUENTA_DE_COBRO": "datetime64[ns]",
    "FECHA_PROGRAMACION_PAGO": "datetime64[ns]",
    "FECHA_REPROGRAMACION_PAGO": "datetime64[ns]",
    "FECHA_PAGO": "datetime64[ns]",
    "FECHA_APROBACION_RUT": "datetime64[ns]",
}


def leer_archivo(file: UploadFile) -> pd.DataFrame:
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="El archivo no tiene nombre.")

        content = BytesIO(file.file.read())
        if file.filename.endswith(".xlsx"):
            return pd.read_excel(content, engine="openpyxl", sheet_name="BASE GENERAL DE CUENTAS")
        elif file.filename.endswith(".csv"):
            return pd.read_csv(content)
        else:
            raise HTTPException(status_code=400, detail="Archivo debe ser .xlsx o .csv")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error leyendo el archivo: {str(e)}")


def columnas_invalidas(row: pd.Series, tipos: dict) -> list:
    errores = []
    for col, tipo_esperado in tipos.items():
        valor = row.get(col)
        if pd.isna(valor):
            continue  # NaN es aceptado
        if tipo_esperado == float:
            if not isinstance(valor, (int, float, np.number)):
                errores.append(col)
        elif tipo_esperado == str:
            if not isinstance(valor, str):
                errores.append(col)
        else:
            if not isinstance(valor, tipo_esperado):
                errores.append(col)
    return errores


def procesar_archivo(file: UploadFile) -> dict:
    df = leer_archivo(file)

    if df.empty:
        raise HTTPException(status_code=400, detail="El archivo está vacío")

    df = df.dropna(subset=["DOCUMENTO"])  # Elimina filas completamente vacías

    columnas_necesarias = list(RENOMBRAR_COLUMNAS.keys()) + [
        "DOCUMENTO",
        "NOMBRE",
        "BANCO",
        "DEPARTAMENTO",
        "MUNICIPIO",
        "ZONA",
        "DSE",
        "RUT",
        "CORREO",
    ]

    df = df[columnas_necesarias]
    df.rename(columns=RENOMBRAR_COLUMNAS, inplace=True)

    # Conversión de fechas
    columnas_fecha = [
        "FECHA_RADICACION_CONTABLE",
        "FECHA_PRESTACION_SERVICIO",
        "FECHA_APROBACION_CUENTA_DE_COBRO",
        "FECHA_APROBACION_SEGURIDAD_SOCIAL",
        "FECHA_APROBACION_RUT",
        "FECHA_CONTRATACION",
        "FECHA_PROGRAMACION_PAGO",
        "FECHA_PAGO",
        "FECHA_REPROGRAMACION_PAGO",
    ]

    for col in columnas_fecha:
        df[col] = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce", dayfirst=True)

    df = df.astype(tipo_columnas)

    # reemplazar valores nulos
    df.replace({np.nan: None}, inplace=True)
    df.replace({"nan": None}, inplace=True)
    df["BANCO"] = df["BANCO"].fillna("SIN VALOR")
    df["MUNICIPIO"] = df["MUNICIPIO"].fillna("SIN VALOR")
    df["MUNICIPIO"] = df["MUNICIPIO"].fillna("SIN VALOR")
    df["ZONA"] = df["ZONA"].fillna("SIN VALOR")
    df["ESTADO_APROBACION_CUENTA_DE_COBRO"] = df["ESTADO_APROBACION_CUENTA_DE_COBRO"].fillna("SIN VALOR")
    df["ESTADO_DE_PAGO"] = df["ESTADO_DE_PAGO"].fillna("SIN VALOR")
    df["ESTADO_DE_REPROGRAMACION"] = df["ESTADO_DE_REPROGRAMACION"].fillna("SIN VALOR")

    return df.head(50).to_dict(orient="index")