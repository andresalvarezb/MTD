import logging
import pandas as pd
from decimal import Decimal
from sqlalchemy.orm import Session
from infraestructura.db.index import get_db
from core.servicios.usuarios.crearCargo import CrearCargo
from core.servicios.cuentasBancarias.crearBanco import CrearBanco
from core.servicios.usuarios.crearUsuario import CrearUsuario
from core.servicios.descuentos.crearDescuento import CrearDescuento
from core.servicios.etlHistorico import procesar_historico
from core.servicios.cuentasBancarias.crearCuentaBancaria import CrearCuentaBancaria
from core.servicios.cuentasPorPagar.crearCuentaPorPagar import CrearCuentaPorPagar
from core.servicios.cuentasPorPagar.obtenerCuentaPorPagar import ObtenerCuentaPorPagar
from app.api.esquemas.cuentaPorPagar import CuentaPorPagarResponseSchema
from core.servicios.cuentasPorPagar.obtenerCuentasPorPagar import ObtenerCuentasPorPagar
from fastapi import APIRouter, UploadFile, File, Depends, status, HTTPException
from core.servicios.historialLaboral.crearHistorialLaboralUsuario import CrearHistorialLaboralUsuario
from infraestructura.db.repositorios.repositorioCargoSqlAlchemy import RepositorioCargoSqlAlchemy
from infraestructura.db.repositorios.repositorioBancoSqlAlchemy import RepositorioBancoSqlAlchemy
from infraestructura.db.repositorios.repositorioUsuarioSqlAlchemy import RepositorioUsuarioSqlAlchemy
from core.servicios.usuarios.crearMunicipio import CrearDepartamento, CrearMunicipio
from infraestructura.db.repositorios.repositorioHistorialLaboralUsuarioSqlAlchemy import (
    RepositorioHistorialLaboralUsuarioSqlAlchemy,
)
from infraestructura.db.repositorios.repositorioMunicipioSqlAlchemy import (
    RepositorioMunicipioSqlAlchemy,
    RepositorioDepartamentoSqlAlchemy,
)


from infraestructura.db.repositorios.repositorioCuentaBancariaSqlAlchemy import (
    RepositorioCuentaBancariaSqlAlchemy,
)
from infraestructura.db.repositorios.repositorioCuentaPorPagarSqlAlchemy import (
    RepositorioCuentaPorPagarSqlAlchemy,
)
from infraestructura.db.repositorios.repositorioDescuentoSQLAlchemy import (
    RepositorioDescuentoSqlAlchemy,
)

from core.servicios.usuarios.dtos import CrearDepartamentoDTO, CrearMunicipioDTO, CrearCargoDTO, CrearUsuarioDTO
from core.servicios.historialLaboral.dtos import CrearHistorialLaboralUsuarioDTO
from core.servicios.cuentasPorPagar.dtos import CrearCuentaPorPagarDTO
from core.servicios.cuentasBancarias.dtos import CrearBancoDTO, CrearCuentaBancariaDTO
from core.servicios.descuentos.dtos import CrearDescuentoDTO
from infraestructura.db.repositorios.repositorioUsuarioSqlAlchemy import RepositorioUsuarioSqlAlchemy

router = APIRouter()


@router.post(
    "/cargar-historial",
    summary="Carga masiva del historial laboral",
    description="""
    Este endpoint permite la **carga masiva** de datos históricos a través de un archivo Excel.
    Cada registro genera entidades como:
    - Usuario
    - Municipio y Departamento
    - Cargo
    - Historial laboral
    - Cuenta bancaria
    - Cuenta por pagar
    - Descuentos asociados

    Los registros procesados exitosamente y los que presenten errores serán devueltos en la respuesta.

    ### Formato esperado del archivo Excel:
    Las columnas deben incluir:
    DOCUMENTO, NOMBRE, BANCO, DEPARTAMENTO, MUNICIPIO, ZONA, DSE, RUT, CORREO, CARGO CONTRATISTA, OPS O NOMINA, ESTADO CONTRATISTA, TELEFONO DE CONTACTO, NO.CUENTA BANCARIA, NÚMERO DE DOCUMENTO CERTIFICADO BANCARIO, EPS PACIENTE ASIGNADO, LIDER ASIGNADO, MES DE RADICACIÓN CONTABLE, FECHA DE SERVICIO, VALOR CUENTA DE COBRO AUTOMATICA, DESCUENTO RETEFUENTE, DESCUENTO TESORERIA, DESCUENTOS VARIOS, VALOR DCTO S.S., TOTAL A PAGAR, ESTADO CUENTA DE COBRO, FECHA APROBACIÓN CUENTA DE COBRO, SEGURIDAD SOCIAL, FECHA APROBACIÓN SEGURIDAD SOCIAL, FECHA APROBACIÓN RUT, FECHA OK CONTRATO, ESTADO REQUISITOS PARA PAGO, FECHA PROGRAMACION, FECHA DE PAGO, ESTADO DE PAGO, CAUSAL DE RECHAZO, FECHA REPROGRAMACIÓN PAGO, ESTADO DE REPROGRAMACIÓN, VALOR MINIMO, DESCUENTO REALIZADO, CANTIDAD DE DESCUENTOS, ACTIVO FIJO O DESCUENTO, VALOR DESCUENTO""",
)
def cargar_historial_cuentas(file: UploadFile = File(...), db: Session = Depends(get_db)):
    registros_fallidos = []
    registros_exitosos = []
    datos = procesar_historico(file)
    for idx, registro in datos.items():
        try:
            # crear la ubciacion del profesional (Municipio, departamento)
            repo_departamento = RepositorioDepartamentoSqlAlchemy(db)
            departamento_service = CrearDepartamento(repo_crear=repo_departamento, repo_obtener=repo_departamento)
            departamento = departamento_service.ejecutar(CrearDepartamentoDTO(nombre=registro["DEPARTAMENTO"]))

            # ! Validar esta exepción
            if departamento.id is None:
                raise Exception("Departamento no encontrado")

            # crear el municipio
            repo_municipio = RepositorioMunicipioSqlAlchemy(db)
            municipio_service = CrearMunicipio(repo_crear=repo_municipio, repo_obtener=repo_municipio)
            municipio = municipio_service.ejecutar(
                CrearMunicipioDTO(nombre=registro["MUNICIPIO"], id_departamento=departamento.id)
            )

            # crear cargo
            repo_cargo = RepositorioCargoSqlAlchemy(db)
            cargo_service = CrearCargo(repo_crear=repo_cargo, repo_obtener=repo_cargo)
            cargo = cargo_service.ejecutar(CrearCargoDTO(nombre=registro["CARGO"]))

            # ! Validar esta exepción
            if cargo.id is None:
                raise Exception("Cargo no encontrado")

            # ! Validar esta exepción
            if municipio.id is None:
                raise Exception("Municipio no encontrado")

            # crear usuario
            repo_usuario = RepositorioUsuarioSqlAlchemy(db)
            usuario_service = CrearUsuario(repo_crear=repo_usuario, repo_obtener=repo_usuario)
            usuario = usuario_service.ejecutar(
                CrearUsuarioDTO(
                    documento=registro["DOCUMENTO"],
                    nombre=registro["NOMBRE"],
                    estado=registro["ESTADO_USUARIO"],  # ? agregrar enum
                    id_municipio=municipio.id,
                    contrato=registro["TIPO_DE_CONTRATO"],
                    id_cargo=cargo.id,
                    correo=registro["CORREO"],
                    telefono=registro["TELEFONO_USUARIO"],
                    seguridad_social=registro["ESTADO_SEGURIDAD_SOCIAL"] == "APROBADO",
                    fecha_aprobacion_seguridad_social=registro["FECHA_APROBACION_SEGURIDAD_SOCIAL"],
                    fecha_ultima_contratacion=registro["FECHA_CONTRATACION"],
                )
            )

            # ! Validar esta exepción
            if usuario.id is None:
                raise Exception("usuario no encontrado")

            # Crear registro del estado del usuario en el historial laboral
            repo_historialLaboralUsuario = RepositorioHistorialLaboralUsuarioSqlAlchemy(db)
            historialLaboralUsuario_service = CrearHistorialLaboralUsuario(
                repo_crear=repo_historialLaboralUsuario, repo_obtener=repo_historialLaboralUsuario
            )
            historialLaboralUsuario = historialLaboralUsuario_service.ejecutar(
                CrearHistorialLaboralUsuarioDTO(
                    id_municipio=municipio.id,
                    contrato=registro["TIPO_DE_CONTRATO"],
                    id_cargo=cargo.id,
                    claveHLU=(
                        str(registro["FECHA_PRESTACION_SERVICIO"].strftime("%Y%m%d"))
                        + str(registro["DOCUMENTO"])
                        + str(registro["FECHA_RADICACION_CONTABLE"].strftime("%Y%m%d"))
                    ),
                    id_usuario=usuario.id,
                    fecha_contratacion=registro["FECHA_CONTRATACION"],
                    seguridad_social=registro["ESTADO_SEGURIDAD_SOCIAL"] == "APROBADO",
                    fecha_aprobacion_seguridad_social=registro["FECHA_APROBACION_SEGURIDAD_SOCIAL"],
                    fecha_ultima_contratacion=registro["FECHA_CONTRATACION"],
                    fecha_fin_contratacion=None,
                )
            )

            # Crear cuenta bancaria
            repo_banco = RepositorioBancoSqlAlchemy(db)
            banco_service = CrearBanco(repo_crear=repo_banco, repo_obtener=repo_banco)
            banco = banco_service.ejecutar(CrearBancoDTO(nombre=registro["BANCO"]))

            # ! Validar esta exepción
            if banco.id is None:
                raise Exception("banco no encontrado")

            repo_cuentaBancaria = RepositorioCuentaBancariaSqlAlchemy(db)
            cuentaBancaria_service = CrearCuentaBancaria(
                repo_crear=repo_cuentaBancaria, repo_obtener=repo_cuentaBancaria
            )
            cuenta_bancaria = cuentaBancaria_service.ejecutar(
                CrearCuentaBancariaDTO(
                    numero_cuenta=registro["NUM_CUENTA_BANCARIA"],
                    numero_certificado=registro["NUM_CERTIFICADO_BANCARIO"],
                    estado="INACTIVA",  # ? agregrar enum
                    id_usuario=usuario.id,
                    id_banco=banco.id,
                    tipo_de_cuenta=None,  # ? agregrar enum
                    fecha_actualizacion=None,
                    observaciones=None,
                )
            )

            # ! Validar esta exepción
            if historialLaboralUsuario.id is None:
                raise Exception("historialLaboralUsuario no encontrado")

            # ! Validar esta exepción
            if cuenta_bancaria.id is None:
                raise Exception("cuenta_bancaria no encontrado")

            # Creacion de la cuenta por pagar
            repo_cuentaPorPagar = RepositorioCuentaPorPagarSqlAlchemy(db)
            cuentaPorPagar_service = CrearCuentaPorPagar(
                repo_crear=repo_cuentaPorPagar, repo_obtener=repo_cuentaPorPagar
            )
            cuenta_por_pagar = cuentaPorPagar_service.ejecutar(
                CrearCuentaPorPagarDTO(
                    id_historial_laboral=historialLaboralUsuario.id,
                    id_cuenta_bancaria=cuenta_bancaria.id,
                    claveCPP=(
                        str(registro["FECHA_PRESTACION_SERVICIO"].strftime("%Y%m%d"))
                        + str(registro["DOCUMENTO"])
                        + str(registro["FECHA_RADICACION_CONTABLE"].strftime("%Y%m%d"))
                    ),
                    fecha_prestacion_servicio=registro["FECHA_PRESTACION_SERVICIO"],
                    fecha_radicacion_contable=registro["FECHA_RADICACION_CONTABLE"],
                    estado_aprobacion_cuenta_usuario=registro["ESTADO_APROBACION_CUENTA_DE_COBRO"],
                    estado_cuenta_por_pagar=registro["ESTADO_REQUISITOS_PARA_PAGO"],
                    valor_cuenta_cobro=registro["VALOR_CUENTA_DE_COBRO"],
                    estado_de_pago=registro["ESTADO_DE_PAGO"],
                    total_descuentos=Decimal(0.0),
                    total_a_pagar=registro["TOTAL_A_PAGAR"],
                    fecha_actualizacion=None,
                    fecha_aprobacion_rut=registro["FECHA_APROBACION_RUT"],
                    fecha_creacion=None,
                    fecha_aprobacion_cuenta_usuario=registro["FECHA_APROBACION_CUENTA_DE_COBRO"],
                    fecha_programacion_pago=registro["FECHA_PROGRAMACION_PAGO"],
                    fecha_reprogramacion=registro["FECHA_REPROGRAMACION_PAGO"],
                    fecha_pago=registro["FECHA_PAGO"],
                    estado_reprogramacion_pago=registro["ESTADO_DE_REPROGRAMACION"],
                    rut=registro["RUT"] == "SI",
                    dse=registro["DSE"],
                    causal_rechazo=registro["CAUSAL_DE_RECHAZO"],
                    creado_por=None,  # ? agregrar enum
                    lider_paciente_asignado=registro["LIDER_ASIGNADO_PACIENTE"],
                    eps_paciente_asignado=registro["EPS_PACIENTE_ASIGNADO"],
                    tipo_de_cuenta=None,
                )
            )

            # Creacion de los descuentos

            descuentos_predefinidos = [
                {
                    "tipo_descuento": "DESCUENTO RETEFUENTE",
                    "valor": (registro.get("DESCUENTO_RETEFUENTE") or 0.0),
                    "descripcion": "",
                },
                {
                    "tipo_descuento": "DESCUENTO SEGURIDAD SOCIAL",
                    "valor": (registro.get("DESCUENTO_SEGURIDAD_SOCIAL") or 0.0),
                    "descripcion": "",
                },
                {
                    "tipo_descuento": "DESCUENTO TESORERIA",
                    "valor": (registro.get("DESCUENTO_TESORERIA") or 0.0),
                    "descripcion": "",
                },
                {
                    "tipo_descuento": "DESCUENTOS_VARIOS",
                    "valor": (registro.get("DESCUENTOS_VARIOS") or 0.0),
                    "descripcion": "",
                },
                {
                    "tipo_descuento": "DESCUENTO_ACTIVOS_FIJOS",
                    "valor": (registro.get("VALOR_DESCUENTO_ACTIVOS_FIJOS") or 0.0),
                    "descripcion": (
                        (registro.get("DESCRIPCION_DESCUENTO_ACTIVOS_FIJOS") or "")
                        + " "
                        + (registro.get("NUMERO_DE_CUOTAS_A_DESCONTAR_ACTIVOS_FIJOS") or "")
                        + " "
                        + (registro.get("OBSERVACION_DESCUENTO_ACTIVOS_FIJOS") or "")
                    ).strip(),
                },
            ]

            # ! Validar esta exepción
            if cuenta_por_pagar.id is None:
                raise Exception("cuenta_por_pagar no encontrado")

            descuentos_creados = []
            for descuento in descuentos_predefinidos:
                if descuento["valor"] == 0.0:
                    continue

                repo_descuentos = RepositorioDescuentoSqlAlchemy(db)
                descuentos_service = CrearDescuento(repo_obtener=repo_descuentos, repo_crear=repo_descuentos)
                descuento_nuevo = descuentos_service.ejecutar(
                    CrearDescuentoDTO(
                        id_cuenta_por_pagar=cuenta_por_pagar.id,
                        id_usuario=usuario.id,
                        id_deuda=None,
                        valor=descuento["valor"],
                        fecha_creacion=registro["FECHA_RADICACION_CONTABLE"],
                        tipo_de_descuento=descuento["tipo_descuento"],
                        descripcion=descuento["descripcion"],
                        fecha_actualizacion=None,
                    )
                )
                descuentos_creados.append(descuento_nuevo)

            # # actualizacion de cueta por pagar
            cuenta_por_pagar.calcular_descuentos(descuentos_creados)
            repo_cuentaPorPagar.actualizar(
                cuenta_por_pagar,
                {
                    "total_descuentos": cuenta_por_pagar.total_descuentos,
                    "total_a_pagar": cuenta_por_pagar.total_a_pagar,
                },
            )

            db.commit()
            registros_exitosos.append(
                {
                    "cuenta_por_pagar": cuenta_por_pagar,
                    "descuentos": descuentos_creados,
                    "cuenta_bancaria": cuenta_bancaria,
                    "banco": banco,
                    "cargo": cargo,
                    "usuario": usuario,
                    "historialLaboralUsuario": historialLaboralUsuario,
                    "municipio": municipio,
                    "departamento": departamento,
                }
            )
        except Exception as e:
            db.rollback()
            logging.warning(f"Error procesando registro {idx}: {e}")
            registro["error"] = str(e)
            registros_fallidos.append(registro)

    if registros_fallidos:
        df_fallidos = pd.DataFrame(registros_fallidos)
        df_fallidos.to_excel("registros_fallidos.xlsx", index=False)

        return {
            # status_code=207,  # Multi-Status (algunos OK, otros no)
            "content": {
                "mensaje": "Se procesaron algunos registros con errores",
                "exitosos": registros_exitosos,
                "fallidos": registros_fallidos,
            }
        }
    return {"message": "Historial cargado correctamente", "data": registros_exitosos}


# @router.get("/", response_model=list[CuentaPorPagarResponseSchema])
# def obtener_cuentas(db: Session = Depends(get_db)):
#     try:
#         repo_cuentasPorPagar = RepositorioCuentaPorPagarSqlAlchemy(db)
#         caso_de_uso = ObtenerCuentasPorPagar(repo_cuentasPorPagar)
#         cuentas = caso_de_uso.ejecutar()
#         cuentas_response = [CuentaPorPagarResponseSchema.model_validate(cuenta) for cuenta in cuentas]
#         return cuentas_response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{id_cuenta_por_pagar}", response_model=CuentaPorPagarResponseSchema)
def obtener_cuenta_por_id(id_cuenta_por_pagar: int, db: Session = Depends(get_db)):
    try:
        repo_cuentasPorPagar = RepositorioCuentaPorPagarSqlAlchemy(db)
        caso_de_uso = ObtenerCuentaPorPagar(repo_cuentasPorPagar)
        cuenta = caso_de_uso.ejecutar(id_cuenta_por_pagar)
        return CuentaPorPagarResponseSchema.model_validate(cuenta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/")
def obtener_cuentas(db: Session = Depends(get_db)):
    try:
        repo_cuentasPorPagar = RepositorioCuentaPorPagarSqlAlchemy(db)
        repo_historialLaboralUsuario = RepositorioHistorialLaboralUsuarioSqlAlchemy(db)
        repo_cuenta_bancaria = RepositorioCuentaBancariaSqlAlchemy(db)
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        repo_municipio = RepositorioMunicipioSqlAlchemy(db)
        repo_departamento = RepositorioDepartamentoSqlAlchemy(db)
        caso_de_uso = ObtenerCuentasPorPagar(
            repo_cuenta_bancaria=repo_cuenta_bancaria,
            repo_cuenta_por_pagar=repo_cuentasPorPagar,
            repo_historial=repo_historialLaboralUsuario,
            repo_usuario=repo_usuario,
            rerpo_municipio=repo_municipio,
            repo_departamento=repo_departamento,
        )
        cuentas = caso_de_uso.ejecutar()
        # cuentas_response = [CuentaPorPagarResponseSchema.model_validate(cuenta) for cuenta in cuentas]
        return cuentas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
