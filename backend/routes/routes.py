# Aquí se crean los controladores y routers para cada entidad usando la fábrica genérica

from http.client import HTTPException
from backend.models.models import *
from backend.controllers.controller import *
from .crud_factory import create_crud_router

# Creación de routers CRUD genéricos para cada entidad
clientes_router = create_crud_router("clientes", clientes_controller, "ci_cliente", Cliente)
proveedores_router = create_crud_router("proveedores", proveedores_controller, "Rif", Proveedor)
productos_router = create_crud_router("productos", productos_controller, "cod_producto", Producto, with_file_upload=True, file_field='img', create_model=ProductoCreate)
ventas_router = create_crud_router("ventas", ventas_controller, "id_ventas", Venta)
tasasCambio_router = create_crud_router("tasasCambio", tasasCambio_controller, "id_tasa", TasaCambio)
categoria_productos_router = create_crud_router("categoria_productos", categoria_productos_controller, "id_categoria", CategoriaProducto)
compras_router = create_crud_router("compras", compras_controller, "id_compra", Compra)
creditos_router = create_crud_router("creditos", creditos_controller, "id_credito", Credito)
pagos_router = create_crud_router("pagos", pagos_controller, "id_pago", Pago)
movimientos_router = create_crud_router("movimientos", movimientos_controller, "id_movimiento", Movimiento)
detalle_venta_router = create_crud_router("detalle_venta", detalle_venta_controller, "id_detalle", DetalleVenta)
productos_preparados_router = create_crud_router("productos_preparados", productos_preparados_controller, "cod_producto_preparado", ProductoPreparado)
productos_noPreparados_router = create_crud_router("productos_noPreparados", productos_noPreparados_controller, "cod_producto_noPreparado", ProductoNoPreparado)

@productos_router.put("/{cod_producto}", response_model=None)
def update(cod_producto: str, producto: Producto):
    print("Actualizando producto:", cod_producto, producto)
    updated = productos_controller.update("cod_producto", cod_producto, producto)
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated

