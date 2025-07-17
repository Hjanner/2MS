from backend.services.services import *
from backend.models.models import *
from .base_controller import BaseController

clientes_controller = BaseController[Cliente](cliente_service)
proveedores_controller = BaseController[Proveedor](proveedor_service)
productos_controller = BaseController[Producto](producto_service)
ventas_controller = BaseController[Venta](venta_service)
tasasCambio_controller = BaseController[TasaCambio](tasaCambio_service)