from fastapi import FastAPI, APIRouter
from .rutas.cuentas import router as cuentas
from .rutas.descuentos import router as descuentos
from .rutas.usuarios import router as usuarios
from .rutas.deuda import router as deudas
from .rutas.areaMTD import router as areas
from fastapi.middleware.cors import CORSMiddleware
from infraestructura.db.index import Base, async_engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Opcional: para borrar todo al reiniciar
        await conn.run_sync(Base.metadata.create_all)
    yield
    # await async_engine.dispose() # Código de cierre (opcional)


app = FastAPI(title="API Cuentas Medicas", description="Uso asincronico", version="0.5.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dominio del frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

router.include_router(cuentas, prefix="/cuentas", tags=["Cuentas por pagar"])
router.include_router(descuentos, prefix="/descuentos", tags=["Descuentos"])
router.include_router(usuarios, prefix="/usuarios", tags=["Usuarios"])
router.include_router(deudas, prefix="/deudas", tags=["Deudas"])
router.include_router(areas, prefix="/areas", tags=["Areas MTD"])


app.include_router(router, prefix="/api")
