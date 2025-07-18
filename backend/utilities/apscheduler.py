from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import asyncio

from backend.services.pydolarve_service import PyDolarVE
from backend.controllers.controller import tasasCambio_controller

# Define la zona horaria de Venezuela
venezuela_tz = pytz.timezone("America/Caracas")

def guardar_tasa_automatica():
    loop = asyncio.get_event_loop()
    try:
        tasa = loop.run_until_complete(PyDolarVE().get_precio_dolar())
        tasasCambio_controller.create(tasa)
        print(f"Tasa guardada automáticamente: {tasa}")
    except Exception as e:
        print(f"Error al guardar la tasa automáticamente: {e}")

# Scheduler
scheduler = BackgroundScheduler(timezone=venezuela_tz)
# Programa la tarea para las 16:00 (4 PM) todos los días
scheduler.add_job(
    guardar_tasa_automatica,
    CronTrigger(hour=16, minute=2)
)
scheduler.start()