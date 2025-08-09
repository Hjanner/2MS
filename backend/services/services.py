from backend.models.models import *
from database.database import db_path
from backend.services.base_service import BaseService

cliente_service = BaseService(Cliente, "Clientes", db_path, unique_fields=["ci_cliente"])
proveedor_service = BaseService(Proveedor, "Proveedores", db_path)
producto_service = BaseService(Producto, "Productos", db_path)
venta_service = BaseService(Venta, "Ventas", db_path)
tasaCambio_service = BaseService(TasaCambio, "TasasCambio", db_path)
categoria_producto_service = BaseService(CategoriaProducto, "Categoria_productos", db_path)
compra_service = BaseService(Compra, "Compras", db_path)
credito_service = BaseService(Credito, "Creditos", db_path)
pago_service = BaseService(Pago, "Pagos", db_path)
movimiento_service = BaseService(Movimiento, "Movimientos", db_path)
detalle_venta_service = BaseService(DetalleVenta, "Detalle_Venta", db_path)
producto_preparado_service = BaseService(ProductoPreparado, "Productos_preparados", db_path)
producto_no_preparado_service = BaseService(ProductoNoPreparado, "Productos_noPreparados", db_path)
