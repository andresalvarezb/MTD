import pytest
from unittest.mock import AsyncMock
from datetime import datetime
from core.entidades.cargo import Cargo
from core.entidades.usuario import Usuario
from core.entidades.municipio import Municipio
from core.servicios.usuarios.dtos import CrearUsuarioDTO
from core.servicios.usuarios.crearUsuario import CrearUsuario
from core.interfaces.repositorioUsuario import CrearUsuarioProtocol, ObtenerUsuarioPorDocumentoProtocol


@pytest.mark.asyncio
async def test_unitario_crear_usuario_exitosamente():
    """
    Este es un test UNITARIO.
    Prueba que el servicio llama a los repositorios correctos cuando el usuario no existe.
    """
    # Arrange / Preparar
    mock_repo_obtener = AsyncMock(spec=ObtenerUsuarioPorDocumentoProtocol)
    mock_repo_crear = AsyncMock(spec=CrearUsuarioProtocol)

    datos_usuario_dto = CrearUsuarioDTO(
        documento="987654321",
        nombre="Test Unitario",
        estado="Activo",
        contrato="Término Fijo",
        cargo=Cargo(nombre="Desarrollador"),
        municipio=Municipio(nombre="Medellín"),
        correo="test.unitario@example.com",
        telefono="555444333",
        seguridad_social=False,
        fecha_aprobacion_seguridad_social=None,
        fecha_ultima_contratacion=None,
    )

    # Configurar los mocks
    # 1. Simular que el usuario NO existe
    # se simula la respuesta de todos los flujos. para poder crear, primero el metodo obtener_por_documento debe retornar None. Es por ello que esto se configura
    mock_repo_obtener.obtener_por_documento.return_value = None

    # 2. Simular la respuesta del repositorio al crear el usuario
    usuario_creado_simulado = Usuario(id=1, **datos_usuario_dto.__dict__)
    mock_repo_crear.crear.return_value = usuario_creado_simulado

    crear_usuario_servicio = CrearUsuario(repo_obtener=mock_repo_obtener, repo_crear=mock_repo_crear)

    # Act / Ejecutar
    resultado = await crear_usuario_servicio.ejecutar(datos_usuario_dto)

    # Assert / Verificar
    # Verificar que el resultado es el que simulamos
    assert resultado == usuario_creado_simulado
    assert resultado.id == 1
    assert resultado.nombre == "TEST UNITARIO"  # Verifica la transformación de la entidad

    # Verificar que los mocks fueron llamados como se esperaba
    mock_repo_obtener.obtener_por_documento.assert_awaited_once_with("987654321")
    mock_repo_crear.crear.assert_awaited_once()


@pytest.mark.asyncio
async def test_unitario_no_recrear_usuario_existecte():
    """
    Este es un test UNITARIO.
    Prueba que si el usuario ya existe, el servicio lo retorna sin intentar crearlo de nuevo.
    """
    # arrange / preparar
    # simular repositorios para obtener y crear usuarios como lo indica el contexto
    mock_repo_obtener = AsyncMock(spec=ObtenerUsuarioPorDocumentoProtocol)
    mock_repo_crear = AsyncMock(spec=CrearUsuarioProtocol)

    datos_usuario_dto = CrearUsuarioDTO(
        documento="111222333",
        nombre="Usuario Existente",
        estado="Activo",
        contrato="OPS",
        cargo=Cargo(nombre="Líder"),
        municipio=Municipio(nombre="Cali"),
        correo="existente@example.com",
        telefono="111222333",
        seguridad_social=True,
        fecha_aprobacion_seguridad_social=datetime.now(),
        fecha_ultima_contratacion=datetime.now(),
    )

    # Configuracion de mocks
    # 1. Simular que el usuario YA existe en la base de datos
    usuario_simulado = Usuario(id=1, **datos_usuario_dto.__dict__)
    mock_repo_obtener.obtener_por_documento.return_value = usuario_simulado
    # 2. No simular la creación, ya que no debería llamarse
    # no se simula la creación porque en el flujo normal no se llama a este método
    crear_usuario_servicio = CrearUsuario(repo_crear=mock_repo_crear, repo_obtener=mock_repo_obtener)

    # Act / Ejecutar
    resultado = await crear_usuario_servicio.ejecutar(datos_usuario_dto)

    # Assert / Verificar
    # Se verifica como deberia estar el retorno
    assert resultado == usuario_simulado

    # Verificar que los mocks fueron llamados como se esperaba, este una sola vez
    mock_repo_obtener.obtener_por_documento.assert_awaited_once_with("111222333")
    # Verificar que el método de crear NO fue llamado, ya que el usuario ya existe
    mock_repo_crear.crear.assert_not_awaited()
