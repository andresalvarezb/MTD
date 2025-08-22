import pytest
from unittest.mock import AsyncMock
from core.entidades.departamento import Departamento
from core.servicios.departamento.dtos import CrearDepartamentoDTO
from core.servicios.departamento.crearDepartamento import CrearDepartamento
from core.interfaces.repositorioDepartamento import CrearDepartamentoProtocol, ObtenerDepartamentoPorNombreProtocol


@pytest.mark.asyncio
async def test_unitario_crear_departamento_exitosamente():
    # * Arrange / Preparar
    # Se crean mocks de los repositorios necesarios
    repo_obtener_departamento = AsyncMock(spec=ObtenerDepartamentoPorNombreProtocol)
    repo_crear_departamento = AsyncMock(spec=CrearDepartamentoProtocol)

    departamento_dto = CrearDepartamentoDTO(nombre="Antioquia")

    # Configurar los mocks
    # 1. Simular que el departamento NO existen
    repo_obtener_departamento.obtener_por_nombre.return_value = None

    departamento_simulado = Departamento(nombre="ANTIOQUIA")
    repo_crear_departamento.crear.return_value = departamento_simulado

    # * Act / Ejecutar
    caso_de_uso = CrearDepartamento(repo_obtener_departamento, repo_crear_departamento)
    resultado = await caso_de_uso.ejecutar(departamento_dto)

    # * Assert / Afirmar
    assert resultado == departamento_simulado

    repo_obtener_departamento.obtener_por_nombre.assert_awaited_once_with("Antioquia")
    repo_crear_departamento.crear.assert_awaited_once_with(Departamento(nombre="Antioquia"))


@pytest.mark.asyncio
async def test_unitario_retornar_departamento_existente():
    # * Arrange / Preparar
    # Se crean mocks de los repositorios necesarios
    repo_obtener_departamento = AsyncMock(spec=ObtenerDepartamentoPorNombreProtocol)
    repo_crear_departamento = AsyncMock(spec=CrearDepartamentoProtocol)

    departamento_dto = CrearDepartamentoDTO(nombre="Antioquia")
    departamento_simulado = Departamento(nombre="ANTIOQUIA")

    # Configurar los mocks
    # 1. Simular que el departamento NO existen
    repo_obtener_departamento.obtener_por_nombre.return_value = departamento_simulado

    # * Act / Ejecutar
    caso_de_uso = CrearDepartamento(repo_obtener_departamento, repo_crear_departamento)
    resultado = await caso_de_uso.ejecutar(departamento_dto)

    # * Assert / Afirmar
    assert resultado == departamento_simulado

    repo_obtener_departamento.obtener_por_nombre.assert_awaited_once_with("Antioquia")
    repo_crear_departamento.crear.assert_not_awaited()
