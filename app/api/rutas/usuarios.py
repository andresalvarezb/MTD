from sqlalchemy.ext.asyncio import AsyncSession
from infraestructura.db.index import get_db
from fastapi import APIRouter, HTTPException, Depends, Path
from core.servicios.usuarios.obtenerUsuario import ObtenerUsuario
from core.servicios.usuarios.crearUsuario import CrearUsuario
from core.servicios.usuarios.obtenerUsuarios import ObtenerUsuarios
from core.servicios.usuarios.actualizarUsuario import ActualizarUsuario
from infraestructura.db.repositorios.repositorioUsuarioSqlAlchemy import RepositorioUsuarioSqlAlchemy
from infraestructura.db.repositorios.repositorioDepartamentoSqlAlchemy import RepositorioDepartamentoSqlAlchemy
from infraestructura.db.repositorios.repositorioCargoSqlAlchemy import RepositorioCargoSqlAlchemy
from infraestructura.db.repositorios.repositorioMunicipioSqlAlchemy import RepositorioMunicipioSqlAlchemy
from app.api.esquemas.usuario import UsuarioCreateSchema, UsuarioResponseSchema, UsuarioUpdateSchema
from core.servicios.usuarios.dtos import (
    CrearUsuarioDTO,
    CrearCargoDTO,
    CrearMunicipioDTO,
    CrearDepartamentoDTO,
    ActualizarUsuarioDTO,
)


router = APIRouter()


@router.post("/", response_model=UsuarioResponseSchema)
async def crear_usuario(usuario: UsuarioCreateSchema, db: AsyncSession = Depends(get_db)):
    try:
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        repo_municipio = RepositorioMunicipioSqlAlchemy(db)
        repo_departamento = RepositorioDepartamentoSqlAlchemy(db)
        repo_cargo = RepositorioCargoSqlAlchemy(db)
        caso_de_uso = CrearUsuario(
            repo_obtener_usuario=repo_usuario,
            repo_crear_usuario=repo_usuario,
            repo_obtener_municipio=repo_municipio,
            repo_crear_municipio=repo_municipio,
            repo_obtener_departamento=repo_departamento,
            repo_crear_departamento=repo_departamento,
            repo_obtener_cargo=repo_cargo,
            repo_crear_cargo=repo_cargo,
        )
        usuario_creado = await caso_de_uso.ejecutar(
            CrearUsuarioDTO(
                documento=usuario.documento,
                nombre=usuario.nombre,
                estado=usuario.estado,
                contrato=usuario.contrato,
                correo=usuario.correo,
                telefono=usuario.telefono,
                cargo=CrearCargoDTO(usuario.cargo),
                municipio=CrearMunicipioDTO(
                    nombre=usuario.municipio,
                    departamento=CrearDepartamentoDTO(nombre=usuario.departamento),
                ),
                seguridad_social=usuario.seguridad_social,
                fecha_aprobacion_seguridad_social=usuario.fecha_aprobacion_seguridad_social,
                fecha_ultima_contratacion=usuario.fecha_ultima_contratacion,
            )
        )
        return usuario_creado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno en Creación de Usuario: {str(e)}")


@router.get("/", response_model=list[UsuarioResponseSchema])
async def obtener_usuarios(
    db: AsyncSession = Depends(get_db),
):
    try:
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        caso_de_uso = ObtenerUsuarios(repo_usuario)
        usuarios = await caso_de_uso.ejecutar()
        return usuarios

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{documento}", response_model=UsuarioResponseSchema)
async def obtener_un_usuario(
    documento: str = Path(
        ...,
        title="Número de documento",
        description="Documento de identidad del usuario a buscar",
        examples=["123456789"],
    ),
    db: AsyncSession = Depends(get_db),
):
    try:
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        caso_de_uso = ObtenerUsuario(repo_usuario)
        usuario = await caso_de_uso.ejecutar(documento)
        return usuario

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno con el usuario {documento}: {str(e)}")


@router.patch("/", response_model=UsuarioResponseSchema)
async def actualizar_usuario(usuario: UsuarioUpdateSchema, db: AsyncSession = Depends(get_db)):
    try:
        repo_usuario = RepositorioUsuarioSqlAlchemy(db)
        caso_de_uso = ActualizarUsuario(repo_usuario, repo_usuario)
        usuario_actualizado = await caso_de_uso.ejecutar(
            ActualizarUsuarioDTO(
                documento=usuario.documento,
                nombre=usuario.nombre,
                estado=usuario.estado,
                contrato=usuario.contrato,
                correo=usuario.correo,
                telefono=usuario.telefono,
                seguridad_social=usuario.seguridad_social,
                fecha_aprobacion_seguridad_social=usuario.fecha_aprobacion_seguridad_social,
                fecha_ultima_contratacion=usuario.fecha_ultima_contratacion,
                cargo=CrearCargoDTO(nombre=usuario.cargo) if usuario.cargo else None,
                municipio=(
                    CrearMunicipioDTO(
                        nombre=usuario.municipio,
                        departamento=CrearDepartamentoDTO(
                            nombre=usuario.departamento if usuario.departamento is not None else ""
                        ),
                    )
                    if usuario.municipio
                    else None
                ),
            )
        )
        return usuario_actualizado

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno en Actualización de Usuario: {str(e)}")
