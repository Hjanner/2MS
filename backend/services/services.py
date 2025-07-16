from backend.models.models import Cliente, Proveedor, Producto
from database.database import db_path
from backend.services.base_service import BaseService

cliente_service = BaseService(Cliente, "Clientes", db_path)
proveedor_service = BaseService(Proveedor, "Proveedores", db_path)
producto_service = BaseService(Producto, "Productos", db_path)

# Agrega aquí más servicios según tus modelos y tablas
