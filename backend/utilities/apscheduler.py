#guarda de manera automatica el cambio de tasa en la base de datos, si esta corriendo el backend
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import asyncio
import nest_asyncio

from backend.services.pydolarve_service import PyDolarVE
from backend.controllers.controller import tasasCambio_controller

nest_asyncio.apply()
# Define la zona horaria de Venezuela
venezuela_tz = pytz.timezone("America/Caracas")

def guardar_tasa_automatica():
    print("[APSCHEDULER] Intentando guardar la tasa automáticamente...")
    try:
        tasa = asyncio.run(PyDolarVE().get_precio_dolar())
        tasasCambio_controller.create(tasa)
        print(f"[APSCHEDULER] Tasa guardada automáticamente: {tasa.valor_usd_bs} (Origen: {tasa.origen})")
    except Exception as e:
        print(f"[APSCHEDULER] Error al guardar la tasa automáticamente: {e}")

# Scheduler
scheduler = BackgroundScheduler(timezone=venezuela_tz)
scheduler.add_job(
    guardar_tasa_automatica,
    CronTrigger(hour='16', minute="01") 
)

print("[APSCHEDULER] Scheduler configurado, esperando inicio...") 
