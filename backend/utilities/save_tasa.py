#script para guardar la tasa de cambio sino se esta ejecutando el backend 
import asyncio
from backend.services.pydolarve_service import PyDolarVE
from backend.controllers.controller import tasasCambio_controller

async def main():
    service = PyDolarVE()
    tasa = await service.get_precio_dolar()
    tasasCambio_controller.create(tasa)
    print("Tasa guardada:", tasa)

if __name__ == "__main__":
    asyncio.run(main())