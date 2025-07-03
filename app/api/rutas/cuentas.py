import logging
import pandas as pd
from io import BytesIO
from decimal import Decimal
from sqlalchemy.orm import Session
from infraestructura.db.index import get_db
from fastapi.responses import StreamingResponse
from core.servicios.cargos.crearCargo import CrearCargo
from core.servicios.cargos.obtenerCargo import ObtenerCargo
from core.servicios.cuentasBancarias.crearBanco import CrearBanco
from core.servicios.usuarios.crearUsuario import CrearUsuario
from core.servicios.descuentos.crearDescuento import CrearDescuento
from core.servicios.etlHistorico import procesar_historico
from core.servicios.cuentasBancarias.crearCuentaBancaria import CrearCuentaBancaria
from core.servicios.cuentasPorPagar.crearCuentaPorPagar import CrearCuentaPorPagar
from core.servicios.cuentasPorPagar.obtenerCuentaPorPagar import ObtenerCuentaPorPagar
from app.api.esquemas.cuentaPorPagar import CuentaPorPagarResponseSchema, CuentaPorPagarUpdateSchema
from core.servicios.cuentasPorPagar.obtenerCuentasPorPagar import ObtenerCuentasPorPagar
from fastapi import APIRouter, UploadFile, File, Depends, status, HTTPException
from core.servicios.historialLaboral.crearHistorialLaboralUsuario import CrearHistorialLaboralUsuario
from core.servicios.historialLaboral.actualizarHistorialLaboral import ActualizarHistorialLaboral
from infraestructura.db.repositorios.repositorioCargoSqlAlchemy import RepositorioCargoSqlAlchemy
from infraestructura.db.repositorios.repositorioBancoSqlAlchemy import RepositorioBancoSqlAlchemy
from infraestructura.db.repositorios.repositorioUsuarioSqlAlchemy import RepositorioUsuarioSqlAlchemy
from core.servicios.municipio.crearMunicipio import CrearMunicipio
from core.servicios.departamento.crearDepartamento import CrearDepartamento
from infraestructura.db.repositorios.repositorioHistorialLaboralUsuarioSqlAlchemy import (
    RepositorioHistorialLaboralUsuarioSqlAlchemy,
)
from infraestructura.db.repositorios.repositorioMunicipioSqlAlchemy import RepositorioMunicipioSqlAlchemy
from infraestructura.db.repositorios.repositorioDepartamentoSqlAlchemy import RepositorioDepartamentoSqlAlchemy


from infraestructura.db.repositorios.repositorioCuentaBancariaSqlAlchemy import (
    RepositorioCuentaBancariaSqlAlchemy,
)
from infraestructura.db.repositorios.repositorioCuentaPorPagarSqlAlchemy import (
    RepositorioCuentaPorPagarSqlAlchemy,
)
from infraestructura.db.repositorios.repositorioDescuentoSQLAlchemy import (
    RepositorioDescuentoSqlAlchemy,
)

from core.servicios.usuarios.dtos import CrearUsuarioDTO, ActualizarUsuarioDTO
from core.servicios.cargos.dtos import CrearCargoDTO, ObtenerCargoDTO
from core.servicios.departamento.dtos import CrearDepartamentoDTO
from core.servicios.municipio.dtos import CrearMunicipioDTO, ObtenerMunicipioDTO
from core.servicios.municipio.dtos import CrearMunicipioDTO
from core.servicios.historialLaboral.dtos import CrearHistorialLaboralUsuarioDTO, ActualizarHistorialLaboralUsuarioDTO
from core.servicios.cuentasPorPagar.dtos import CrearCuentaPorPagarDTO, ActualizarCuentaPorPagarDTO
from core.servicios.cuentasBancarias.dtos import (
    CrearBancoDTO,
    CrearCuentaBancariaDTO,
    ActualizarCuentaBancariaDTO,
    ObtenerBancoDTO,
)
from core.servicios.descuentos.dtos import CrearDescuentoDTO
from infraestructura.db.repositorios.repositorioUsuarioSqlAlchemy import RepositorioUsuarioSqlAlchemy
from core.servicios.municipio.ObtenerMunicipio import ObtenerMunicipio
from core.servicios.usuarios.actualizarUsuario import ActualizarUsuario
from core.servicios.historialLaboral.actualizarHistorialLaboral import ActualizarHistorialLaboral
from core.servicios.cuentasBancarias.actualizarCuentaBancaria import ActualizarCuentaBancaria
from core.servicios.cuentasBancarias.obtenerBanco import ObtenerBanco
from core.servicios.cuentasPorPagar.actualizarCuentaPorPagar import ActualizarCuentaPorPagar
from core.entidades.usuario import Usuario
from core.entidades.historialLaboralUsuario import HistorialLaboralUsuario
from app.api.esquemas.historialLaboralUsuario import HistorialLaboralUpdateSchema
from app.api.esquemas.usuario import UsuarioUpdateSchema
from app.api.esquemas.municipio import MunicipioUpdateSchema
from app.api.esquemas.cargo import CargoUpdateSchema
from app.api.esquemas.cuentaBancaria import CuentaBancariaUpdateSchema, BancoUpdateSchema
from core.entidades.cuentaBancaria import CuentaBancaria
from core.entidades.cuentaPorPagar import CuentaPorPagar
from core.entidades.banco import Banco


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

            # crear el municipio
            repo_municipio = RepositorioMunicipioSqlAlchemy(db)
            municipio_service = CrearMunicipio(repo_crear=repo_municipio, repo_obtener=repo_municipio)
            municipio = municipio_service.ejecutar(
                CrearMunicipioDTO(nombre=registro["MUNICIPIO"], departamento=departamento)
            )

            # crear cargo
            repo_cargo = RepositorioCargoSqlAlchemy(db)
            cargo_service = CrearCargo(repo_crear=repo_cargo, repo_obtener=repo_cargo)
            cargo = cargo_service.ejecutar(CrearCargoDTO(nombre=registro["CARGO"]))

            # crear usuario
            repo_usuario = RepositorioUsuarioSqlAlchemy(db)
            usuario_service = CrearUsuario(repo_crear=repo_usuario, repo_obtener=repo_usuario)
            usuario = usuario_service.ejecutar(
                CrearUsuarioDTO(
                    documento=registro["DOCUMENTO"],
                    nombre=registro["NOMBRE"],
                    estado=registro["ESTADO_USUARIO"],  # ? agregrar enum
                    municipio=municipio,
                    contrato=registro["TIPO_DE_CONTRATO"],
                    cargo=cargo,
                    correo=registro["CORREO"],
                    telefono=registro["TELEFONO_USUARIO"],
                    seguridad_social=registro["ESTADO_SEGURIDAD_SOCIAL"] == "APROBADO",
                    fecha_aprobacion_seguridad_social=registro["FECHA_APROBACION_SEGURIDAD_SOCIAL"],
                    fecha_ultima_contratacion=registro["FECHA_CONTRATACION"],
                )
            )

            # Crear registro del estado del usuario en el historial laboral
            repo_historialLaboralUsuario = RepositorioHistorialLaboralUsuarioSqlAlchemy(db)
            historialLaboralUsuario_service = CrearHistorialLaboralUsuario(
                repo_crear=repo_historialLaboralUsuario, repo_obtener=repo_historialLaboralUsuario
            )
            historialLaboralUsuario = historialLaboralUsuario_service.ejecutar(
                CrearHistorialLaboralUsuarioDTO(
                    usuario=usuario,
                    cargo=cargo,
                    municipio=municipio,
                    contrato=registro["TIPO_DE_CONTRATO"],
                    claveHLU=(
                        str(registro["FECHA_PRESTACION_SERVICIO"].strftime("%Y%m%d"))
                        + str(registro["DOCUMENTO"])
                        + str(registro["FECHA_RADICACION_CONTABLE"].strftime("%Y%m%d"))
                    ),
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

            repo_cuentaBancaria = RepositorioCuentaBancariaSqlAlchemy(db)
            cuentaBancaria_service = CrearCuentaBancaria(
                repo_crear=repo_cuentaBancaria, repo_obtener=repo_cuentaBancaria
            )
            cuenta_bancaria = cuentaBancaria_service.ejecutar(
                CrearCuentaBancariaDTO(
                    usuario=usuario,
                    banco=banco,
                    numero_cuenta=registro["NUM_CUENTA_BANCARIA"],
                    numero_certificado=registro["NUM_CERTIFICADO_BANCARIO"],
                    estado="INACTIVA",  # ? agregrar enum
                    tipo_de_cuenta="AHORROS",  # ? agregrar enum
                    fecha_actualizacion=None,
                    observaciones=None,
                )
            )

            # Creacion de la cuenta por pagar
            repo_cuentaPorPagar = RepositorioCuentaPorPagarSqlAlchemy(db)
            cuentaPorPagar_service = CrearCuentaPorPagar(
                repo_crear=repo_cuentaPorPagar, repo_obtener=repo_cuentaPorPagar
            )
            cuenta_por_pagar = cuentaPorPagar_service.ejecutar(
                CrearCuentaPorPagarDTO(
                    claveCPP=(
                        str(registro["FECHA_PRESTACION_SERVICIO"].strftime("%Y%m%d"))
                        + str(registro["DOCUMENTO"])
                        + str(registro["FECHA_RADICACION_CONTABLE"].strftime("%Y%m%d"))
                    ),
                    historial_laboral=historialLaboralUsuario,
                    cuenta_bancaria=cuenta_bancaria,
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

            descuentos_creados = []
            for descuento in descuentos_predefinidos:
                if descuento["valor"] == 0.0:
                    continue

                repo_descuentos = RepositorioDescuentoSqlAlchemy(db)
                descuentos_service = CrearDescuento(repo_obtener=repo_descuentos, repo_crear=repo_descuentos)
                descuento_nuevo = descuentos_service.ejecutar(
                    CrearDescuentoDTO(
                        usuario=usuario,
                        cuenta_por_pagar=cuenta_por_pagar,
                        deuda=None,
                        valor=descuento["valor"],
                        fecha_creacion=registro["FECHA_RADICACION_CONTABLE"],
                        tipo_de_descuento=descuento["tipo_descuento"],
                        descripcion=descuento["descripcion"],
                        fecha_actualizacion=None,
                    )
                )
                descuentos_creados.append(descuento_nuevo)

            # # actualizacion de cuenta por pagar
            cuenta_por_pagar.calcular_descuentos(descuentos_creados)
            # repo_cuentaPorPagar.actualizar(
            #     cuenta_por_pagar,
            #     {
            #         "total_descuentos": cuenta_por_pagar.total_descuentos,
            #         "total_a_pagar": cuenta_por_pagar.total_a_pagar,
            #     },
            # )
            cuenta_por_pagar.total_descuentos = cuenta_por_pagar.total_descuentos
            cuenta_por_pagar.total_a_pagar = cuenta_por_pagar.total_a_pagar
            repo_cuentaPorPagar.actualizar(cuenta_por_pagar)

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
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_fallidos.to_excel(writer, index=False, sheet_name="Errores")
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=registros_fallidos.xlsx",
                "Content-Type": "application/octet-stream",
            },
        )
    return {"message": f"Se han cargado {len(registros_exitosos)} registros exitosamente"}


@router.get("/", response_model=list[CuentaPorPagarResponseSchema])
def obtener_cuentas(db: Session = Depends(get_db)):
    try:
        repo_cuentasPorPagar = RepositorioCuentaPorPagarSqlAlchemy(db)
        caso_de_uso = ObtenerCuentasPorPagar(repo_cuentasPorPagar)
        cuentas = caso_de_uso.ejecutar()
        return cuentas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{id_cuenta}", response_model=CuentaPorPagarResponseSchema)
def obtener_cuenta_por_id(id_cuenta: int, db: Session = Depends(get_db)):
    try:
        repo_cuentasPorPagar = RepositorioCuentaPorPagarSqlAlchemy(db)
        caso_de_uso = ObtenerCuentaPorPagar(repo_cuentasPorPagar)
        cuenta = caso_de_uso.ejecutar(id_cuenta)
        return cuenta
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.patch("/{id_cuenta}", response_model=CuentaPorPagarResponseSchema)
# @router.patch("/{id_cuenta}")
def actualizar_cuenta_por_id(id_cuenta: int, registro: CuentaPorPagarUpdateSchema, db: Session = Depends(get_db)):
    try:
        # obtener cuenta de la base de datos
        repo_cuentasPorPagar = RepositorioCuentaPorPagarSqlAlchemy(db)
        caso_de_uso = ObtenerCuentaPorPagar(repo_cuentasPorPagar)
        cuenta_por_pagar_bd = caso_de_uso.ejecutar(id_cuenta)

        # destructura el registro que llega, compararlo con la data de la base y actualizar
        historial_actualizado = None
        cuenta_bancaria_actualizada = None
        municipio_actualizado = None
        cargo_actualizado = None
        usuario_actualizado = None

        # obtener nuevo municipio
        if registro.historial_laboral:

            if registro.historial_laboral.municipio and registro.historial_laboral.municipio.nombre:
                repo_municipio = RepositorioMunicipioSqlAlchemy(db)
                caso_de_uso_municipio = ObtenerMunicipio(repo_municipio)
                municipio_actualizado = caso_de_uso_municipio.ejecutar(
                    ObtenerMunicipioDTO(nombre=registro.historial_laboral.municipio.nombre)
                )
                # historial["municipio"]=municipio

            # obtener nuevo cargo
            if registro.historial_laboral.cargo and registro.historial_laboral.cargo.nombre:
                repo_cargo = RepositorioCargoSqlAlchemy(db)
                caso_de_uso_cargo = ObtenerCargo(repo_cargo)
                cargo_actualizado = caso_de_uso_cargo.ejecutar(
                    ObtenerCargoDTO(nombre=registro.historial_laboral.cargo.nombre)
                )
                # historial["cargo"]=cargo

            # actualizar usuario
            if registro.historial_laboral.usuario:
                repo_usuario = RepositorioUsuarioSqlAlchemy(db)
                caso_de_uso_usuario = ActualizarUsuario(repo_actualizar=repo_usuario, repo_obtener=repo_usuario)
                usuario_actualizado = caso_de_uso_usuario.ejecutar(
                    info_nueva=ActualizarUsuarioDTO(
                        documento=registro.historial_laboral.usuario.documento,
                        nombre=registro.historial_laboral.usuario.nombre,
                        estado=registro.historial_laboral.usuario.estado,
                        contrato=registro.historial_laboral.usuario.contrato,
                        correo=registro.historial_laboral.usuario.correo,
                        telefono=registro.historial_laboral.usuario.telefono,
                        seguridad_social=registro.historial_laboral.seguridad_social,
                        fecha_aprobacion_seguridad_social=registro.historial_laboral.fecha_aprobacion_seguridad_social,
                        cargo=cargo_actualizado,
                        municipio=municipio_actualizado,
                    ),
                    info_vieja=Usuario(**cuenta_por_pagar_bd.historial_laboral.usuario.model_dump()),
                )

            # actualizar historial laboral
            repo_historialLaboral = RepositorioHistorialLaboralUsuarioSqlAlchemy(db)
            caso_de_uso_historial = ActualizarHistorialLaboral(
                repo_actualizar=repo_historialLaboral, repo_obtener=repo_historialLaboral
            )
            historial_actualizado = caso_de_uso_historial.ejecutar(
                info_nueva=ActualizarHistorialLaboralUsuarioDTO(
                    usuario=usuario_actualizado,
                    contrato=registro.historial_laboral.contrato,
                    cargo=cargo_actualizado,
                    municipio=municipio_actualizado,
                    seguridad_social=registro.historial_laboral.seguridad_social,
                    fecha_contratacion=registro.historial_laboral.fecha_contratacion,
                    fecha_fin_contratacion=registro.historial_laboral.fecha_fin_contratacion,
                    fecha_ultima_contratacion=registro.historial_laboral.fecha_ultima_contratacion,
                    fecha_aprobacion_seguridad_social=registro.historial_laboral.fecha_aprobacion_seguridad_social,
                ),
                info_vieja=HistorialLaboralUsuario(**cuenta_por_pagar_bd.historial_laboral.model_dump()),
            )

        if registro.cuenta_bancaria:
            banco_actualizado = None
            if registro.cuenta_bancaria.banco and registro.cuenta_bancaria.banco.nombre:
                # actualizar banco
                repo_banco = RepositorioBancoSqlAlchemy(db)
                caso_de_uso_banco = ObtenerBanco(repo_banco)
                banco_actualizado = caso_de_uso_banco.ejecutar(
                    ObtenerBancoDTO(nombre=registro.cuenta_bancaria.banco.nombre)
                )

            # actualizar cuenta bancaria
            repo_cuenta_bancaria = RepositorioCuentaBancariaSqlAlchemy(db)
            caso_de_uso_cuenta = ActualizarCuentaBancaria(
                repo_actualizar=repo_cuenta_bancaria, repo_obtener=repo_cuenta_bancaria
            )

            cuenta_bancaria_actualizada = caso_de_uso_cuenta.ejecutar(
                info_nueva=ActualizarCuentaBancariaDTO(
                    usuario=usuario_actualizado,
                    banco=banco_actualizado,
                    numero_certificado=registro.cuenta_bancaria.numero_certificado,
                    estado=registro.cuenta_bancaria.estado,
                    tipo_de_cuenta=registro.cuenta_bancaria.tipo_de_cuenta,
                    observaciones=registro.cuenta_bancaria.observaciones,
                ),
                info_vieja=CuentaBancaria(
                    numero_cuenta=cuenta_por_pagar_bd.cuenta_bancaria.numero_cuenta,
                    numero_certificado=cuenta_por_pagar_bd.cuenta_bancaria.numero_certificado,
                    estado=cuenta_por_pagar_bd.cuenta_bancaria.estado,
                    usuario=Usuario(**cuenta_por_pagar_bd.historial_laboral.usuario.model_dump()),
                    banco=Banco(**cuenta_por_pagar_bd.cuenta_bancaria.banco.model_dump()),
                    id=cuenta_por_pagar_bd.cuenta_bancaria.id,
                    tipo_de_cuenta=cuenta_por_pagar_bd.cuenta_bancaria.tipo_de_cuenta,
                    fecha_actualizacion=cuenta_por_pagar_bd.cuenta_bancaria.fecha_actualizacion,
                    observaciones=cuenta_por_pagar_bd.cuenta_bancaria.observaciones,
                ),
            )

        # actualizar cuenta por pagar
        repo_cuenta_por_pagar = RepositorioCuentaPorPagarSqlAlchemy(db)
        caso_de_uso_cuenta = ActualizarCuentaPorPagar(
            repo_actualizar=repo_cuenta_por_pagar, repo_obtener=repo_cuenta_por_pagar
        )
        cuenta_por_pagar = caso_de_uso_cuenta.ejecutar(
            info_nueva=ActualizarCuentaPorPagarDTO(
                historial_laboral=historial_actualizado,
                cuenta_bancaria=cuenta_bancaria_actualizada,
                estado_aprobacion_cuenta_usuario=registro.estado_aprobacion_cuenta_usuario,
                valor_cuenta_cobro=registro.valor_cuenta_cobro,
                estado_de_pago=registro.estado_de_pago,
                fecha_aprobacion_rut=registro.fecha_aprobacion_rut,
                fecha_aprobacion_cuenta_usuario=registro.fecha_aprobacion_cuenta_usuario,
                fecha_programacion_pago=registro.fecha_programacion_pago,
                fecha_reprogramacion=registro.fecha_reprogramacion,
                fecha_pago=registro.fecha_pago,
                estado_reprogramacion_pago=registro.estado_reprogramacion_pago,
                rut=registro.rut,
                dse=registro.dse,
                causal_rechazo=registro.causal_rechazo,
                lider_paciente_asignado=registro.lider_paciente_asignado,
                eps_paciente_asignado=registro.eps_paciente_asignado,
            ),
            info_vieja=CuentaPorPagar(**cuenta_por_pagar_bd.model_dump()),
        )
        db.commit()

        # obtener cuenta por pagar
        cuenta_actualizada = obtener_cuenta_por_id(id_cuenta, db)
        return cuenta_actualizada
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
