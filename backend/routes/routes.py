# Archivo de orquestación de routers para las entidades principales
# Aquí se crean los controladores y routers para cada entidad usando la fábrica genérica

from backend.controllers.base_controller import BaseController
from backend.services.services import cliente_service, proveedor_service
from backend.models.models import Cliente, Proveedor
from .crud_factory import create_crud_router

# Instanciación de controladores base para cada entidad
clientes_controller = BaseController[Cliente](cliente_service)
proveedores_controller = BaseController[Proveedor](proveedor_service)

# Creación de routers CRUD genéricos para cada entidad
clientes_router = create_crud_router("clientes", clientes_controller, "ci_cliente", Cliente)
proveedores_router = create_crud_router("proveedores", proveedores_controller, "Rif", Proveedor)

# Puedes agregar aquí más routers para otras entidades siguiendo el mismo patrón