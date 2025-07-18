# Endpoint para obtener el precio del dólar
from fastapi import APIRouter, HTTPException
from backend.controllers.controller import tasasCambio_controller
from backend.models.models import TasaCambio
from backend.services.pydolarve_service import PyDolarVE

api_utils_router = APIRouter()

@api_utils_router.get("/dolar", tags=["TasasCambio"], summary="Obtener precio actual del dólar (PyDolarVE)", response_model=TasaCambio)
async def obtener_precio_dolar():
    service = PyDolarVE()
    try:
        tasa = await service.get_precio_dolar()
        return tasa
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

@api_utils_router.get("/dolar/guardar", tags=["TasasCambio"], summary="Guardar precio actual del dólar (PyDolarVE)", response_model=TasaCambio)
async def guardar_precio_dolar():
    dolar_service = PyDolarVE()
    try:
        tasa = await dolar_service.get_precio_dolar()
        tasaG = tasasCambio_controller.create(tasa)
        print(tasaG)
        if tasaG is None:
            raise HTTPException(status_code=500, detail="No se pudo guardar la tasa de cambio")            
        return tasaG
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
