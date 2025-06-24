from fastapi import APIRouter
from .rutas.cuentas import router as cuentas
from .rutas.descuentos import router as descuentos
from .rutas.seguridadSocial import router as seguridadSocial
from .rutas.usuarios import router as usuarios
from fastapi import FastAPI


router = APIRouter()

router.include_router(cuentas, prefix="/cuentas", tags=["Cuentas por pagar"])
router.include_router(descuentos, prefix="/descuentos", tags=["Descuentos"])
router.include_router(usuarios, prefix="/usuarios", tags=["Usuarios"])
router.include_router(seguridadSocial, prefix="/seguridad-social", tags=["Seguridad Social"])




app = FastAPI(title="API Cuentas Medicas", description="", version="0.1.0")
