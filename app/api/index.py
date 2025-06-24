from fastapi import APIRouter
from .rutas.cuentas import router as cuentas
from .rutas.descuentos import router as descuentos
from fastapi import FastAPI


router = APIRouter()

router.include_router(cuentas, prefix="/cuentas", tags=["cuentasPorPagar"])
router.include_router(descuentos, prefix="/descuentos", tags=["descuentos"])


app = FastAPI(title="API Cuentas Medicas", description="", version="0.1.0")
