# from apscheduler.schedulers.background import BackgroundScheduler

# def guardar_tasa_automatica():
#     import asyncio
#     loop = asyncio.get_event_loop()
#     tasa = loop.run_until_complete(PyDolarVE().get_precio_dolar())
#     tasasCambio_controller.create(tasa)

# scheduler = BackgroundScheduler()
# scheduler.add_job(guardar_tasa_automatica, 'interval', hours=1)
# scheduler.start()