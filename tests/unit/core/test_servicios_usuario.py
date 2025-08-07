import pytest
from dataclasses import asdict
from unittest.mock import AsyncMock
from datetime import datetime
from core.entidades.cargo import Cargo
from core.entidades.usuario import Usuario
from core.entidades.municipio import Municipio
from core.entidades.departamento import Departamento
from core.servicios.usuarios.dtos import (
    CrearUsuarioDTO,
    ActualizarUsuarioDTO,
    CrearCargoDTO,
    CrearMunicipioDTO,
    CrearDepartamentoDTO,
)
from core.servicios.usuarios.crearUsuario import CrearUsuario
from core.interfaces.repositorioUsuario import (
    CrearUsuarioProtocol,
    ObtenerUsuarioPorDocumentoProtocol,
    ActualizarUsuarioProtocol,
)
from core.servicios.usuarios.actualizarUsuario import ActualizarUsuario
from core.servicios.usuarios.obtenerUsuario import ObtenerUsuario
from utils.enums import EnumEstadoUsuario
from core.interfaces.repositorioMunicipio import CrearMunicipioProtocol, ObtenerMunicipioPorNombreProtocol
from core.interfaces.repositorioDepartamento import CrearDepartamentoProtocol, ObtenerDepartamentoPorNombreProtocol
from core.interfaces.repositorioCargo import CrearCargoProtocol, ObtenerCargoPorNombreProtocol


# * TEST UNITARIO PARA EL SERVICIO DE CREACIÓN DE USUARIOS
@pytest.mark.asyncio
async def test_unitario_crear_usuario_exitosamente():
    """
    Este test verifica que el caso de uso CrearUsuario crea
    un usuario y sus dependencias (cargo, municipio, departamento)
    cuando ninguna de ellas existe previamente.
    """
    # * Arrange / Preparar
    # Se crean mocks de los repositorios necesarios
    repo_obtener_usuario = AsyncMock(spec=ObtenerUsuarioPorDocumentoProtocol)
    repo_crear_usuario = AsyncMock(spec=CrearUsuarioProtocol)
    repo_obtener_municipio = AsyncMock(spec=ObtenerMunicipioPorNombreProtocol)
    repo_crear_municipio = AsyncMock(spec=CrearMunicipioProtocol)
    repo_obtener_departamento = AsyncMock(spec=ObtenerDepartamentoPorNombreProtocol)
    repo_crear_departamento = AsyncMock(spec=CrearDepartamentoProtocol)
    repo_obtener_cargo = AsyncMock(spec=ObtenerCargoPorNombreProtocol)
    repo_crear_cargo = AsyncMock(spec=CrearCargoProtocol)

    # Se define un DTO con los datos del usuario a crear
    datos_usuario_dto = CrearUsuarioDTO(
        documento="987654321",
        nombre="Test Unitario",
        estado="Activo",
        contrato="nomina",
        cargo=CrearCargoDTO(nombre="Desarrollador"),
        municipio=CrearMunicipioDTO(nombre="Medellin", departamento=CrearDepartamentoDTO(nombre="Antioquia")),
        correo="test.unitario@example.com",
        telefono="5554443",
        seguridad_social=False,
        fecha_aprobacion_seguridad_social=None,
        fecha_ultima_contratacion=None,
    )

    # Configurar los mocks
    # 1. Simular que el usuario, cargo, departamento y municipio NO existen, es decir, se debe crear todo
    repo_obtener_usuario.obtener_por_documento.return_value = None
    repo_obtener_cargo.obtener_por_nombre.return_value = None
    repo_obtener_departamento.obtener_por_nombre.return_value = None
    repo_obtener_municipio.obtener_por_nombre.return_value = None

    # 2. Simular las respuestas de los repositorios al crear el usuario
    cargo_simulado = Cargo(
        # id=1,
        nombre="DESARROLLADOR"
    )
    departamento_simulado = Departamento(
        # id=1,
        nombre="ANTIOQUIA"
    )
    municipio_simulado = Municipio(
        # id=1,
        nombre="MEDELLIN",
        departamento=departamento_simulado,
    )
    usuario_simulado = Usuario(
        # id=1,
        nombre="TEST UNITARIO",
        documento="987654321",
        estado="ACTIVO",
        contrato="NOMINA",
        cargo=cargo_simulado,
        municipio=municipio_simulado,
        correo="test.unitario@example.com",
        telefono="5554443",
        seguridad_social=False,
        fecha_aprobacion_seguridad_social=None,
        fecha_ultima_contratacion=None,
    )

    repo_crear_cargo.crear.return_value = cargo_simulado
    repo_crear_departamento.crear.return_value = departamento_simulado
    repo_crear_municipio.crear.return_value = municipio_simulado
    repo_crear_usuario.crear.return_value = usuario_simulado

    # 3. Instanciar el caso de uso con los mocks
    caso_de_uso = CrearUsuario(
        repo_obtener_usuario=repo_obtener_usuario,
        repo_crear_usuario=repo_crear_usuario,
        repo_obtener_municipio=repo_obtener_municipio,
        repo_crear_municipio=repo_crear_municipio,
        repo_obtener_departamento=repo_obtener_departamento,
        repo_crear_departamento=repo_crear_departamento,
        repo_obtener_cargo=repo_obtener_cargo,
        repo_crear_cargo=repo_crear_cargo,
    )

    # * Act / Ejecutar
    resultado = await caso_de_uso.ejecutar(datos_usuario_dto)

    print(f"Resultado: {resultado}")
    print(f"Esperado: {usuario_simulado}")
    print(f"Tipo resultado: {type(resultado)}")

    # * Assert / Verificar
    # Verificar que el resultado es el que simulamos
    assert resultado == usuario_simulado

    # Verificar que los mocks fueron llamados como se esperaba
    repo_obtener_usuario.obtener_por_documento.assert_awaited_once_with("987654321")
    repo_obtener_cargo.obtener_por_nombre.assert_awaited_once_with("Desarrollador")
    repo_obtener_departamento.obtener_por_nombre.assert_awaited_once_with("Antioquia")
    repo_obtener_municipio.obtener_por_nombre.assert_awaited_once_with("Medellin")

    repo_crear_usuario.crear.assert_awaited_once_with(usuario_simulado)
    repo_crear_cargo.crear.assert_awaited_once_with(cargo_simulado)
    repo_crear_departamento.crear.assert_awaited_once_with(departamento_simulado)
    repo_crear_municipio.crear.assert_awaited_once_with(municipio_simulado)


@pytest.mark.asyncio
async def test_unitario_retornar_usuario_existente():
    """
    Este es un test UNITARIO.
    Prueba que si el usuario ya existe, el servicio lo retorna sin intentar crearlo de nuevo.
    """
    # * Arrange / Preparar
    repo_obtener_usuario = AsyncMock(spec=ObtenerUsuarioPorDocumentoProtocol)
    repo_crear_usuario = AsyncMock(spec=CrearUsuarioProtocol)
    repo_obtener_municipio = AsyncMock(spec=ObtenerMunicipioPorNombreProtocol)
    repo_crear_municipio = AsyncMock(spec=CrearMunicipioProtocol)
    repo_obtener_departamento = AsyncMock(spec=ObtenerDepartamentoPorNombreProtocol)
    repo_crear_departamento = AsyncMock(spec=CrearDepartamentoProtocol)
    repo_obtener_cargo = AsyncMock(spec=ObtenerCargoPorNombreProtocol)
    repo_crear_cargo = AsyncMock(spec=CrearCargoProtocol)

    datos_usuario_dto = CrearUsuarioDTO(
        documento="987654321",
        nombre="Test Unitario",
        estado="Activo",
        contrato="nomina",
        cargo=CrearCargoDTO(nombre="Desarrollador"),
        municipio=CrearMunicipioDTO(nombre="Medellin", departamento=CrearDepartamentoDTO(nombre="Antioquia")),
        correo="test.unitario@example.com",
        telefono="5554443",
        seguridad_social=False,
        fecha_aprobacion_seguridad_social=None,
        fecha_ultima_contratacion=None,
    )

    cargo_simulado = Cargo(nombre="DESARROLLADOR")
    departamento_simulado = Departamento(nombre="ANTIOQUIA")
    municipio_simulado = Municipio(nombre="MEDELLIN", departamento=departamento_simulado)
    usuario_simulado = Usuario(
        nombre="TEST UNITARIO",
        documento="987654321",
        estado="ACTIVO",
        contrato="NOMINA",
        cargo=cargo_simulado,
        municipio=municipio_simulado,
        correo="test.unitario@example.com",
        telefono="5554443",
        seguridad_social=False,
        fecha_aprobacion_seguridad_social=None,
        fecha_ultima_contratacion=None,
    )

    repo_obtener_usuario.obtener_por_documento.return_value = usuario_simulado

    caso_de_uso = CrearUsuario(
        repo_obtener_usuario=repo_obtener_usuario,
        repo_crear_usuario=repo_crear_usuario,
        repo_obtener_municipio=repo_obtener_municipio,
        repo_crear_municipio=repo_crear_municipio,
        repo_obtener_departamento=repo_obtener_departamento,
        repo_crear_departamento=repo_crear_departamento,
        repo_obtener_cargo=repo_obtener_cargo,
        repo_crear_cargo=repo_crear_cargo,
    )

    # * Act / Ejecutar
    resultado = await caso_de_uso.ejecutar(datos_usuario_dto)

    # * Assert / Verificar
    assert resultado == usuario_simulado
    repo_obtener_usuario.obtener_por_documento.assert_awaited_once_with("987654321")

    # Asegurar que no se llamaron los métodos de creación ni de obtención adicional
    repo_crear_usuario.crear.assert_not_awaited()
    repo_obtener_cargo.obtener_por_nombre.assert_not_awaited()
    repo_crear_cargo.crear.assert_not_awaited()
    repo_obtener_departamento.obtener_por_nombre.assert_not_awaited()
    repo_crear_departamento.crear.assert_not_awaited()
    repo_obtener_municipio.obtener_por_nombre.assert_not_awaited()
    repo_crear_municipio.crear.assert_not_awaited()


@pytest.mark.asyncio
async def test_unitario_crear_usuario_municipio_nuevo():
    # * Arrange / Preparar
    # Se crean mocks de los repositorios necesarios
    repo_obtener_usuario = AsyncMock(spec=ObtenerUsuarioPorDocumentoProtocol)
    repo_crear_usuario = AsyncMock(spec=CrearUsuarioProtocol)
    repo_obtener_municipio = AsyncMock(spec=ObtenerMunicipioPorNombreProtocol)
    repo_crear_municipio = AsyncMock(spec=CrearMunicipioProtocol)
    repo_obtener_departamento = AsyncMock(spec=ObtenerDepartamentoPorNombreProtocol)
    repo_crear_departamento = AsyncMock(spec=CrearDepartamentoProtocol)
    repo_obtener_cargo = AsyncMock(spec=ObtenerCargoPorNombreProtocol)
    repo_crear_cargo = AsyncMock(spec=CrearCargoProtocol)

    # Se define un DTO con los datos del usuario a crear
    datos_usuario_dto = CrearUsuarioDTO(
        documento="123456789",
        nombre="Juan Prueba",
        estado="Activo",
        contrato="nomina",
        cargo=CrearCargoDTO(nombre="Desarrollador"),
        municipio=CrearMunicipioDTO(nombre="La Ceja", departamento=CrearDepartamentoDTO(nombre="Antioquia")),
        correo="juan.prueba@example.com",
        telefono="1234567",
        seguridad_social=True,
        fecha_aprobacion_seguridad_social=datetime(2024, 7, 1),
        fecha_ultima_contratacion=datetime(2024, 6, 1),
    )

    # Simulacion
    repo_obtener_usuario.obtener_por_documento.return_value = None  # Usuario no existe

    cargo_simulado = Cargo(nombre="DESARROLLADOR")
    departamento_simulado = Departamento(nombre="ANTIOQUIA")
    municipio_simulado = Municipio(nombre="LA CEJA", departamento=departamento_simulado)
    usuario_simulado = Usuario(
        nombre="JUAN PRUEBA",
        documento="123456789",
        estado="ACTIVO",
        contrato="NOMINA",
        cargo=cargo_simulado,
        municipio=municipio_simulado,
        correo="juan.prueba@example.com",
        telefono="1234567",
        seguridad_social=True,
        fecha_aprobacion_seguridad_social=datetime(2024, 7, 1),
        fecha_ultima_contratacion=datetime(2024, 6, 1),
    )

    repo_obtener_cargo.obtener_por_nombre.return_value = cargo_simulado
    repo_obtener_departamento.obtener_por_nombre.return_value = departamento_simulado
    repo_obtener_municipio.obtener_por_nombre.return_value = None  # Municipio no existe
    repo_crear_municipio.crear.return_value = municipio_simulado
    repo_crear_usuario.crear.return_value = usuario_simulado

    # Instancia del caso de uso
    caso_de_uso = CrearUsuario(
        repo_obtener_usuario=repo_obtener_usuario,
        repo_crear_usuario=repo_crear_usuario,
        repo_obtener_municipio=repo_obtener_municipio,
        repo_crear_municipio=repo_crear_municipio,
        repo_obtener_departamento=repo_obtener_departamento,
        repo_crear_departamento=repo_crear_departamento,
        repo_obtener_cargo=repo_obtener_cargo,
        repo_crear_cargo=repo_crear_cargo,
    )

    # * Act
    resultado = await caso_de_uso.ejecutar(datos_usuario_dto)

    # * Assert
    assert resultado == usuario_simulado

    repo_obtener_usuario.obtener_por_documento.assert_awaited_once_with("123456789")
    repo_obtener_cargo.obtener_por_nombre.assert_awaited_once_with("Desarrollador")
    repo_obtener_departamento.obtener_por_nombre.assert_awaited_once_with("Antioquia")
    repo_obtener_municipio.obtener_por_nombre.assert_awaited_once_with("La Ceja")
    repo_crear_municipio.crear.assert_awaited_once()
    repo_crear_usuario.crear.assert_awaited_once()

    # Verificar que no se crearon cargo ni departamento
    repo_crear_cargo.crear.assert_not_awaited()
    repo_crear_departamento.crear.assert_not_awaited()


@pytest.mark.asyncio
async def test_unitario_crear_usuario_cargo_nuevo():
    # * Arrange / Preparar
    # Se crean mocks de los repositorios necesarios
    repo_obtener_usuario = AsyncMock(spec=ObtenerUsuarioPorDocumentoProtocol)
    repo_crear_usuario = AsyncMock(spec=CrearUsuarioProtocol)
    repo_obtener_municipio = AsyncMock(spec=ObtenerMunicipioPorNombreProtocol)
    repo_crear_municipio = AsyncMock(spec=CrearMunicipioProtocol)
    repo_obtener_departamento = AsyncMock(spec=ObtenerDepartamentoPorNombreProtocol)
    repo_crear_departamento = AsyncMock(spec=CrearDepartamentoProtocol)
    repo_obtener_cargo = AsyncMock(spec=ObtenerCargoPorNombreProtocol)
    repo_crear_cargo = AsyncMock(spec=CrearCargoProtocol)

    # Se define un DTO con los datos del usuario a crear
    datos_usuario_dto = CrearUsuarioDTO(
        documento="123456789",
        nombre="Juan Prueba",
        estado="Activo",
        contrato="nomina",
        cargo=CrearCargoDTO(nombre="Desarrollador"),
        municipio=CrearMunicipioDTO(nombre="La Ceja", departamento=CrearDepartamentoDTO(nombre="Antioquia")),
        correo="juan.prueba@example.com",
        telefono="1234567",
        seguridad_social=True,
        fecha_aprobacion_seguridad_social=datetime(2024, 7, 1),
        fecha_ultima_contratacion=datetime(2024, 6, 1),
    )

    # Simulacion
    repo_obtener_usuario.obtener_por_documento.return_value = None  # Usuario no existe

    cargo_simulado = Cargo(nombre="DESARROLLADOR")
    departamento_simulado = Departamento(nombre="ANTIOQUIA")
    municipio_simulado = Municipio(nombre="LA CEJA", departamento=departamento_simulado)
    usuario_simulado = Usuario(
        nombre="JUAN PRUEBA",
        documento="123456789",
        estado="ACTIVO",
        contrato="NOMINA",
        cargo=cargo_simulado,
        municipio=municipio_simulado,
        correo="juan.prueba@example.com",
        telefono="1234567",
        seguridad_social=True,
        fecha_aprobacion_seguridad_social=datetime(2024, 7, 1),
        fecha_ultima_contratacion=datetime(2024, 6, 1),
    )

    repo_obtener_cargo.obtener_por_nombre.return_value = None  # Cargo no existe
    repo_obtener_departamento.obtener_por_nombre.return_value = departamento_simulado
    repo_obtener_municipio.obtener_por_nombre.return_value = municipio_simulado
    repo_crear_cargo.crear.return_value = cargo_simulado
    repo_crear_usuario.crear.return_value = usuario_simulado

    # Instancia del caso de uso
    caso_de_uso = CrearUsuario(
        repo_obtener_usuario=repo_obtener_usuario,
        repo_crear_usuario=repo_crear_usuario,
        repo_obtener_municipio=repo_obtener_municipio,
        repo_crear_municipio=repo_crear_municipio,
        repo_obtener_departamento=repo_obtener_departamento,
        repo_crear_departamento=repo_crear_departamento,
        repo_obtener_cargo=repo_obtener_cargo,
        repo_crear_cargo=repo_crear_cargo,
    )

    # * Act
    resultado = await caso_de_uso.ejecutar(datos_usuario_dto)

    # * Assert
    assert resultado == usuario_simulado

    repo_obtener_usuario.obtener_por_documento.assert_awaited_once_with("123456789")
    repo_obtener_cargo.obtener_por_nombre.assert_awaited_once_with("Desarrollador")
    repo_obtener_departamento.obtener_por_nombre.assert_awaited_once_with("Antioquia")
    repo_obtener_municipio.obtener_por_nombre.assert_awaited_once_with("La Ceja")
    repo_crear_cargo.crear.assert_awaited_once_with(cargo_simulado)
    repo_crear_usuario.crear.assert_awaited_once()

    # Verificar que no se crearon municipio ni departamento
    repo_crear_departamento.crear.assert_not_awaited()
    repo_crear_municipio.crear.assert_not_awaited()


# * TEST UNITARIO PARA OBTENER USUARIO
@pytest.mark.asyncio
async def test_obtener_usuario_encontrado():
    # * Arrange / Preparar
    # Se crean mocks de los repositorios necesarios
    repo_mock = AsyncMock(spec=ObtenerUsuarioPorDocumentoProtocol)

    cargo_simulado = Cargo(
        # id=1,
        nombre="DESARROLLADOR"
    )
    departamento_simulado = Departamento(
        # id=1,
        nombre="ANTIOQUIA"
    )
    municipio_simulado = Municipio(
        # id=1,
        nombre="MEDELLIN",
        departamento=departamento_simulado,
    )
    usuario_simulado = Usuario(
        # id=1,
        nombre="TEST UNITARIO",
        documento="987654321",
        estado="ACTIVO",
        contrato="NOMINA",
        cargo=cargo_simulado,
        municipio=municipio_simulado,
        correo="test.unitario@example.com",
        telefono="5554443",
        seguridad_social=False,
        fecha_aprobacion_seguridad_social=None,
        fecha_ultima_contratacion=None,
    )

    # Configurar los mocks
    repo_mock.obtener_por_documento.return_value = usuario_simulado

    caso_uso = ObtenerUsuario(repo_mock)

    # * Act
    resultado = await caso_uso.ejecutar("123456789")

    # Assert
    assert resultado == usuario_simulado
    repo_mock.obtener_por_documento.assert_awaited_once_with("123456789")


@pytest.mark.asyncio
async def test_obtener_usuario_no_encontrado():
    # Arrange
    repo_mock = AsyncMock(spec=ObtenerUsuarioPorDocumentoProtocol)
    repo_mock.obtener_por_documento.return_value = None

    caso_uso = ObtenerUsuario(repo_mock)

    # Act & Assert
    with pytest.raises(ValueError, match="Usuario no encontrado"):
        await caso_uso.ejecutar("000000000")

    repo_mock.obtener_por_documento.assert_awaited_once_with("000000000")


# * TEST UNITARIO PARA ACTUALIZAR UN USUARIO


@pytest.mark.asyncio
async def test_actualizar_usuario_exitosamente():
    # * Arrange

    # Se crean mocks de los repositorios necesarios
    repo_actualizar = AsyncMock(spec=ActualizarUsuarioProtocol)
    repo_obtener = AsyncMock(spec=ObtenerUsuarioPorDocumentoProtocol)

    usuario_existente = Usuario(
        documento="12345678",
        nombre="Juan",
        estado="ACTIVO",
        contrato="NOMINA",
        cargo=Cargo(nombre="DESARROLLADOR"),
        municipio=Municipio(nombre="MEDELLIN", departamento=Departamento(nombre="ANTIOQUIA")),
        correo="juan@example.com",
        telefono="1234567",
        seguridad_social=True,
        fecha_aprobacion_seguridad_social=datetime(2024, 8, 1),
        fecha_ultima_contratacion=datetime(2024, 6, 1),
    )

    usuario_actualizado = Usuario(
        documento="12345678",
        nombre="JUAN ACTUALIZADO",
        estado="INACTIVO",
        contrato="NOMINA",
        cargo=Cargo(nombre="DESARROLLADOR"),
        municipio=Municipio(nombre="MEDELLIN", departamento=Departamento(nombre="ANTIOQUIA")),
        correo="juan.actualizado@example.com",
        telefono="7654321",
        seguridad_social=False,
        fecha_aprobacion_seguridad_social=datetime(2024, 8, 1),
        fecha_ultima_contratacion=datetime(2024, 7, 1),
    )

    # simulacion
    repo_obtener.obtener_por_documento.return_value = usuario_existente
    repo_actualizar.actualizar.return_value = usuario_actualizado

    # Se define un DTO con los datos del usuario a actualizar
    info_nueva = ActualizarUsuarioDTO(
        documento="12345678", nombre="JUAN ACTUALIZADO", correo="juan.actualizado@example.com"
    )

    # * Act
    caso_de_uso = ActualizarUsuario(repo_actualizar, repo_obtener)

    resultado = await caso_de_uso.ejecutar(info_nueva)

    # * Assert
    assert resultado == usuario_actualizado
    repo_obtener.obtener_por_documento.assert_awaited_once_with("12345678")
    repo_actualizar.actualizar.assert_awaited_once_with(asdict(info_nueva), usuario_existente)


@pytest.mark.asyncio
async def test_actualizar_usuario_no_encontrado():
    # * Arrange

    # Se crean mocks de los repositorios necesarios
    repo_actualizar = AsyncMock(spec=ActualizarUsuarioProtocol)
    repo_obtener = AsyncMock(spec=ObtenerUsuarioPorDocumentoProtocol)

    # simulacion
    repo_obtener.obtener_por_documento.return_value = None

    # Se define un DTO con los datos del usuario a actualizar
    info_nueva = ActualizarUsuarioDTO(
        documento="12345678", nombre="JUAN ACTUALIZADO", correo="juan.actualizado@example.com"
    )

    # * Act
    caso_de_uso = ActualizarUsuario(repo_actualizar, repo_obtener)

    # * Assert
    with pytest.raises(ValueError, match="Usuario no encontrado. No se puede actualizar"):
        await caso_de_uso.ejecutar(info_nueva)

    repo_obtener.obtener_por_documento.assert_awaited_once_with("12345678")
    repo_actualizar.actualizar.assert_not_awaited()
