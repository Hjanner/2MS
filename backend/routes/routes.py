# Aquí se crean los controladores y routers para cada entidad usando la fábrica genérica

from backend.models.models import *
from backend.controllers.controller import *
from .crud_factory import create_crud_router
from backend.services.pydolarve_service import PyDolarVE

# Creación de routers CRUD genéricos para cada entidad
clientes_router = create_crud_router("clientes", clientes_controller, "ci_cliente", Cliente)
proveedores_router = create_crud_router("proveedores", proveedores_controller, "Rif", Proveedor)
productos_router = create_crud_router("productos", productos_controller, "id_producto", Producto)
ventas_router = create_crud_router("ventas", ventas_controller, "id_ventas", Venta)
tasasCambio_router = create_crud_router("tasasCambio", tasasCambio_controller, "id_tasa", TasaCambio)
categoria_productos_router = create_crud_router("categoria_productos", categoria_productos_controller, "id_categoria", CategoriaProducto)
compras_router = create_crud_router("compras", compras_controller, "id_compra", Compra)
creditos_router = create_crud_router("creditos", creditos_controller, "id_credito", Credito)
pagos_router = create_crud_router("pagos", pagos_controller, "id_pago", Pago)
inventarios_router = create_crud_router("inventarios", inventarios_controller, "id_inventario", Inventario)
detalle_venta_router = create_crud_router("detalle_venta", detalle_venta_controller, "id_detalle", DetalleVenta)
compra_inventario_router = create_crud_router("compra_inventario", compra_inventario_controller, ["id_compra", "id_inventario", "cod_producto"], CompraInventario)
productos_preparados_router = create_crud_router("productos_preparados", productos_preparados_controller, "cod_producto_preparado", ProductoPreparado)
productos_noPreparados_router = create_crud_router("productos_noPreparados", productos_noPreparados_controller, "cod_producto_noPreparado", ProductoNoPreparado)
