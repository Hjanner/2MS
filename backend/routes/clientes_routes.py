from fastapi import APIRouter, HTTPException
from backend.controllers.clientes_controller import ClientesController
from backend.models.models import Cliente
from typing import List

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=List[Cliente])
def listar_clientes():
    return ClientesController.get_all_clientes()

@router.get("/{ci_cliente}", response_model=Cliente)
def obtener_cliente(ci_cliente: str):
    cliente = ClientesController.get_cliente_by_id(ci_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/", response_model=None, status_code=201)
def crear_cliente(cliente: Cliente):
    ClientesController.create_cliente(cliente)
    return {"mensaje": "Cliente creado exitosamente"}

@router.put("/{ci_cliente}", response_model=None)
def actualizar_cliente(ci_cliente: str, cliente: Cliente):
    actualizado = ClientesController.update_cliente(ci_cliente, cliente)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"mensaje": "Cliente actualizado exitosamente"}

@router.delete("/{ci_cliente}", response_model=None)
def eliminar_cliente(ci_cliente: str):
    eliminado = ClientesController.delete_cliente(ci_cliente)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"mensaje": "Cliente eliminado exitosamente"} 