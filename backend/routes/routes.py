from backend.controllers.base_controller import BaseController
from backend.services.services import cliente_service, proveedor_service
from backend.models.models import Cliente, Proveedor

clientes_controller = BaseController[Cliente](cliente_service)
proveedores_controller = BaseController[Proveedor](proveedor_service)

from .crud_factory import create_crud_router

clientes_router = create_crud_router("clientes", clientes_controller, "ci_cliente", Cliente)
proveedores_router = create_crud_router("proveedores", proveedores_controller, "Rif", Proveedor)