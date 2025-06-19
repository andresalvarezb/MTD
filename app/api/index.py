from fastapi import APIRouter
from .rutas.cuentas import router as cuentas
from fastapi import FastAPI


router = APIRouter()

router.include_router(cuentas, prefix="/cuentas", tags=["cuentasPorPagar"])


app = FastAPI(title="API Cuentas Medicas", description="", version="0.1.0")
