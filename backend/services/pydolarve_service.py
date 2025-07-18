from datetime import datetime
import httpx 
from backend.models.models import TasaCambio
from backend.services.base_service import BaseService

class PyDolarVE: 
    """
    Clase PyDolarVE para interactuar con la API de PyDolarVE.
    """
    
    BASE_URL = "https://pydolarve.org/"
    
    async def get_data(self, endpoint: str = 'api/v2/tipo-cambio', params: dict = {"currency": "usd"}):
        # headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()

    async def get_precio_dolar(self): 
        data = await self.get_data()
        print(data)
        if data:
            valor_usd_bs = data['price']
            fecha_str = data['last_update'].strip()  # '18/07/2025, 12:00 AM'
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y, %I:%M %p")  
            origen = 'BCV'
            
            return TasaCambio(
                id_tasa=None,
                fecha=fecha,
                valor_usd_bs=valor_usd_bs,
                origen=origen
            )
        else:
            return ("No se pudo obtener el precio del dólar del API de PyDolarVE")
