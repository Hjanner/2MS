from backend.models.models import *
from database.database import db_path
from backend.services.base_service import BaseService

cliente_service = BaseService(Cliente, "Clientes", db_path)
proveedor_service = BaseService(Proveedor, "Proveedores", db_path)
producto_service = BaseService(Producto, "Productos", db_path)
venta_service = BaseService(Venta, "Ventas", db_path)
tasaCambio_servcie = BaseService(TasaCambio, "TasasCambio", db_path)

