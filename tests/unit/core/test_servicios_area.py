import pytest
from unittest.mock import AsyncMock
from core.interfaces.repositorioAreaMTD import CrearAreaMTDProtocol, ObtenerAreaPorNombreProtocol
from core.entidades.areaMtd import AreaMTD
from core.servicios.areaMTD.crearAreaMTD import CrearAreaMTD


@pytest.mark.asyncio
async def test_crear_area_mtd_exitosamente():
    # Arrange
    repo_crear = AsyncMock(spec=CrearAreaMTDProtocol)
    repo_obtener = AsyncMock(spec=ObtenerAreaPorNombreProtocol)

    repo_obtener.obtener_por_nombre.return_value = None  # Simula que no existe el área

    area_simulada = AreaMTD("AREA DE PRUEBA")
    repo_crear.crear.return_value = area_simulada

    # Act
    caso_de_uso = CrearAreaMTD(repo_crear, repo_obtener)
    resultado = await caso_de_uso.ejecutar("area de prueba")

    # Assert
    assert resultado == area_simulada

    repo_obtener.obtener_por_nombre.assert_awaited_once_with("area de prueba")
    repo_crear.crear.assert_awaited_once_with(AreaMTD("area de prueba"))


@pytest.mark.asyncio
async def test_retornar_area_mtd_existente():
    # Arrange
    repo_crear = AsyncMock(spec=CrearAreaMTDProtocol)
    repo_obtener = AsyncMock(spec=ObtenerAreaPorNombreProtocol)

    area_simulada = AreaMTD("AREA DE PRUEBA")
    repo_obtener.obtener_por_nombre.return_value = area_simulada

    # Act
    caso_de_uso = CrearAreaMTD(repo_crear, repo_obtener)
    resultado = await caso_de_uso.ejecutar("area de prueba")

    # Assert
    assert resultado == area_simulada

    repo_obtener.obtener_por_nombre.assert_awaited_once_with("area de prueba")
    repo_crear.crear.assert_not_awaited()