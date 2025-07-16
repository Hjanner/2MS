from backend.models.models import Cliente
from database.database import db_path
from backend.services.base_service import BaseService

class ClienteService(BaseService):
    def __init__(self, db_path: str = db_path):
        super().__init__(Cliente, "Clientes", db_path) 