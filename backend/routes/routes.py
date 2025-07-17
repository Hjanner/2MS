# Archivo de orquestación de routers para las entidades principales
# Aquí se crean los controladores y routers para cada entidad usando la fábrica genérica

from backend.models.models import *
from backend.controllers.controller import *
from .crud_factory import create_crud_router


# Creación de routers CRUD genéricos para cada entidad
clientes_router = create_crud_router("clientes", clientes_controller, "ci_cliente", Cliente)
proveedores_router = create_crud_router("proveedores", proveedores_controller, "Rif", Proveedor)
productos_router = create_crud_router("productos", productos_controller, "id_producto", Producto)
ventas_router = create_crud_router("ventas", ventas_controller, "id_ventas", Venta)
tasasCambio_router = create_crud_router("tasasCambio", tasasCambio_controller, "id_tasa", TasaCambio)