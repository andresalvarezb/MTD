import pytest
from datetime import datetime
from core.entidades.cargo import Cargo
from core.entidades.municipio import Municipio
from core.servicios.usuarios.dtos import CrearUsuarioDTO
from core.servicios.usuarios.crearUsuario import CrearUsuario


@pytest.mark.asyncio
async def test_crear_usuario_integracion(repositorio_usuario):
    """Este es un test de INTEGRACIÓN porque usa un repositorio real y una base de datos."""
    # Arrange / preparar
    crear_usuario_servicio = CrearUsuario(repo_obtener=repositorio_usuario, repo_crear=repositorio_usuario)
    datos_usuario = CrearUsuarioDTO(
        documento="123456789",
        nombre="Hugo Plata",
        estado="Activo",
        contrato="OPS",
        cargo=Cargo(nombre="auxiliar de enfermería"),
        municipio=Municipio(nombre="Bogotá"),
        correo="hugo.plata@example.com",
        telefono="1234567890",
        seguridad_social=True,
        fecha_aprobacion_seguridad_social=datetime.strptime("2023-01-01", "%Y-%m-%d"),
        fecha_ultima_contratacion=datetime.strptime("2023-01-01", "%Y-%m-%d"),
    )
    # Act / ejecutar
    resultado = await crear_usuario_servicio.ejecutar(datos_usuario)

    # Assert / verificar
    assert resultado is not None
    assert resultado.documento == datos_usuario.documento
    assert resultado.nombre == datos_usuario.nombre.upper()
    assert resultado.estado == datos_usuario.estado.upper()
    assert resultado.municipio.nombre == datos_usuario.municipio.nombre.upper()
    assert resultado.contrato == datos_usuario.contrato.upper()
    assert resultado.cargo.nombre == datos_usuario.cargo.nombre.upper()
    assert resultado.correo == datos_usuario.correo.lower()
    assert resultado.telefono == datos_usuario.telefono
    assert resultado.seguridad_social == datos_usuario.seguridad_social
    assert resultado.fecha_aprobacion_seguridad_social == datos_usuario.fecha_aprobacion_seguridad_social
    assert resultado.fecha_ultima_contratacion == datos_usuario.fecha_ultima_contratacion
