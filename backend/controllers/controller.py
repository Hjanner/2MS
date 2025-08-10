from backend.controllers.compras_controller import VistaComprasController
from backend.models.view_models import ProductoVista
from backend.services.services import *
from backend.models.models import *
from .base_controller import BaseController

clientes_controller = BaseController[Cliente](cliente_service)
proveedores_controller = BaseController[Proveedor](proveedor_service)
productos_controller = BaseController[Producto](producto_service)
ventas_controller = BaseController[Venta](venta_service)
tasasCambio_controller = BaseController[TasaCambio](tasaCambio_service)
categoria_productos_controller = BaseController[CategoriaProducto](categoria_producto_service)
compras_controller = BaseController[Compra](compra_service)
creditos_controller = BaseController[Credito](credito_service)
pagos_controller = BaseController[Pago](pago_service)
movimientos_controller = BaseController[Movimiento](movimiento_service)
detalle_venta_controller = BaseController[DetalleVenta](detalle_venta_service)
productos_preparados_controller = BaseController[ProductoPreparado](producto_preparado_service)
productos_noPreparados_controller = BaseController[ProductoNoPreparado](producto_no_preparado_service)

vistaProductosController = BaseController[ProductoVista](vistaProductos_service)
vistaComprasController = VistaComprasController(vistaCompras_service)