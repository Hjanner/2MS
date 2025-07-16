from backend.services.services import cliente_service, proveedor_service
from backend.models.models import Cliente, Proveedor
from base_controller import BaseController

clientes_controller = BaseController[Cliente](cliente_service)
proveedores_controller = BaseController[Proveedor](proveedor_service)