from backend.services.clientes_service import ClienteService
from backend.models.models import Cliente
from typing import List, Optional

cliente_service = ClienteService()

class ClientesController:
    @staticmethod
    def get_all_clientes() -> List[Cliente]:
        return cliente_service.get_all()

    @staticmethod
    def get_cliente_by_id(ci_cliente: str) -> Optional[Cliente]:
        return cliente_service.get_by_id("ci_cliente", ci_cliente)

    @staticmethod
    def create_cliente(cliente: Cliente) -> None:
        cliente_service.create(cliente)

    @staticmethod
    def update_cliente(ci_cliente: str, cliente: Cliente) -> bool:
        return cliente_service.update("ci_cliente", ci_cliente, cliente)

    @staticmethod
    def delete_cliente(ci_cliente: str) -> bool:
        return cliente_service.delete("ci_cliente", ci_cliente) 