from fastapi import APIRouter
from .rutas.cuentas import router as cuentas
from .rutas.descuentos import router as descuentos
from .rutas.usuarios import router as usuarios
from .rutas.deuda import router as deudas
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Cuentas Medicas", description="", version="0.1.0")

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


app.include_router(router, prefix="/api")
