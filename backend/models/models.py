import sqlite3
from fastapi import UploadFile
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import date, datetime
from backend.validators.mixins import *

class Cliente(BaseModel, ClienteValidators):
    """
    Modelo para la tabla 'Clientes' .
    Representa a un cliente con su información personal.
    """
    ci_cliente: str = Field(..., description="Cédula de Identidad del cliente (clave primaria)")
    nombre: str = Field(..., description="Nombre completo del cliente")
    tlf: Optional[str] = Field(None, description="Número de teléfono del cliente (opcional)")
    depto_escuela: Optional[str] = Field(None, description="Departamento o escuela del cliente (opcional)")

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la instancia del modelo en un diccionario ('s model_dump)."""
        return self.model_dump() 

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Cliente':
        """Crea una instancia del modelo desde un diccionario ()."""
        return Cliente(**data)

    def __repr__(self) -> str:
        return f"Cliente(CI: {self.ci_cliente}, Nombre: {self.nombre})"

class TasaCambio(BaseModel, TasaCambioValidators):
    """
    Modelo para la tabla 'TasasCambio' .
    Registra las tasas de cambio de USD a BS en una fecha específica y su origen.
    """
    id_tasa: Optional[int] = Field(None, description="ID único de la tasa de cambio (AUTOINCREMENT)")
    fecha: datetime = Field(..., description="Fecha y hora de la tasa de cambio")
    valor_usd_bs: float = Field(..., description="Valor de 1 USD en Bolívares")
    origen: str = Field(..., description="Origen de la tasa ('BCV' o 'Manual')")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode='json') # 'json' mode para serializar dates a ISO format

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TasaCambio':
        return TasaCambio(**data)

    def __repr__(self) -> str:
        return f"TasaCambio(ID: {self.id_tasa}, Fecha: {self.fecha}, Valor: {self.valor_usd_bs})"

class Venta(BaseModel, VentaValidators):
    """
    Modelo para la tabla 'Ventas' .
    Registra cada transacción de venta.
    """
    id_venta: Optional[int] = Field(None, description="ID único de la venta (AUTOINCREMENT)")
    monto_total_bs: float = Field(..., description="Monto total de la venta en Bolívares")
    fecha: date = Field(..., description="Fecha de la venta")
    monto_total_usd: float = Field(..., description="Monto total de la venta en Dólares")
    tipo: str = Field(..., description="Tipo de venta ('credito' o 'de_contado')")
    ci_cliente: Optional[str] = Field(None, description="CI del cliente asociado a la venta (opcional)")
    id_tasa: Optional[int] = Field(None, description="ID de la tasa de cambio utilizada (opcional)")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode='json')

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Venta':
        return Venta(**data)

    def __repr__(self) -> str:
        return f"Venta(ID: {self.id_venta}, Fecha: {self.fecha}, Monto BS: {self.monto_total_bs})"

class CategoriaProducto(BaseModel):
    """
    Modelo para la tabla 'categoria_productos' .
    Clasifica los productos en preparados o no preparados.
    """
    id_categoria: Optional[int] = Field(None, description="ID único de la categoría (AUTOINCREMENT)")
    descr: str = Field(..., description="Descripción de la categoría")
    tipo: str = Field(..., description="Tipo de categoría ('preparado' o 'noPreparado')")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CategoriaProducto':
        return CategoriaProducto(**data)

    def __repr__(self) -> str:
        return f"CategoriaProducto(ID: {self.id_categoria}, Descripción: {self.descr}, Tipo: {self.tipo})"

class Proveedor(BaseModel, ProveedorValidators):
    """
    Modelo para la tabla 'Proveedores' .
    Almacena la información de los proveedores.
    """
    Rif: str = Field(..., description="RIF del proveedor (clave primaria)")
    razon_social: str = Field(..., description="Razón social del proveedor")
    direccion: Optional[str] = Field(None, description="Dirección del proveedor (opcional)")
    tfl: Optional[str] = Field(None, description="Teléfono del proveedor (opcional)")
    persona_contacto: Optional[str] = Field(None, description="Persona de contacto del proveedor (opcional)")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Proveedor':
        return Proveedor(**data)

    def __repr__(self) -> str:
        return f"Proveedor(Rif: {self.Rif}, Razón Social: {self.razon_social})"

class ProductoBase(BaseModel, ProductoValidators):
    """
    Modelo para la tabla 'Productos' .
    Información general de un producto.
    """
    cod_producto: str = Field(..., description="Código único del producto")
    nombre: str = Field(..., description="Nombre del producto")
    precio_usd: float = Field(..., description="Precio del producto")
    id_categoria: Optional[int] = Field(None, description="ID de la categoría")
    
class ProductoCreate(ProductoBase):
    """
    Modelo de la tabla Producto para entrada (creación con archivo).
    """
    img: UploadFile = Field(..., description="Archivo de imagen del producto. Solo para recepción en el contexto de una petición HTTP.")

class Producto(ProductoBase):
    """
    Modelo de la tabla Producto para salida y base de datos
    """
    img: Optional[str] = Field(..., description="URL de la imagen del producto")
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Producto':
        return Producto(**data)

    def __repr__(self) -> str:
        return f"Producto(Código: {self.cod_producto}, Nombre: {self.nombre}, Precio: {self.precio})"

class ProductoPreparado(BaseModel, ProductoPreparadoValidators):
    """
    Modelo para la tabla 'Productos_preparados' .
    Extiende la información de un producto si es preparado.
    """
    cod_producto_preparado: str = Field(..., description="Código del producto preparado (clave primaria y foránea)")
    descr: str = Field(..., description="Descripcion del producto preparado.")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ProductoPreparado':
        return ProductoPreparado(**data)

    def __repr__(self) -> str:
        return f"ProductoPreparado(Código: {self.cod_producto_preparado})"

class ProductoNoPreparado(BaseModel, ProductoNoPreparadoValidators):
    """
    Modelo para la tabla 'Productos_noPreparados' .
Extiende la información de un producto si no es preparado (inventariable).
    """
    cod_producto_noPreparado: str = Field(..., description="Código del producto no preparado (clave primaria y foránea)")
    cant_min: int = Field(..., description="Cantidad mínima en inventario para alerta")
    cant_actual: int = Field(..., description="Cantidad actual en inventario")
    costo_compra: float = Field(..., description="Costo de compra unitario del producto")
    unidad_medida: str = Field(..., description="Unidad de medida del producto (ej. 'kg', 'unidad')")
    Rif: Optional[str] = Field(None, description="RIF del proveedor asociado al producto (clave foránea)")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ProductoNoPreparado':
        return ProductoNoPreparado(**data)

    def __repr__(self) -> str:
        return f"ProductoNoPreparado(Código: {self.cod_producto_noPreparado}, Actual: {self.cant_actual})"

class Compra(BaseModel):
    """
    Modelo para la tabla 'Compras' .
    Registra una compra a un proveedor.
    """
    id_compra: Optional[int] = Field(None, description="ID único de la compra (AUTOINCREMENT)")
    fecha: date = Field(..., description="Fecha de la compra")
    Rif: str = Field(..., description="RIF del proveedor de la compra (clave foránea)")
    gasto_total: float = Field(..., description="Gasto total de la compra.")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode='json')

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Compra':
        return Compra(**data)

    def __repr__(self) -> str:
        return f"Compra(ID: {self.id_compra}, Fecha: {self.fecha}, Proveedor Rif: {self.Rif})"

class Credito(BaseModel):
    """
    Modelo para la tabla 'Creditos' .
    Gestiona los créditos otorgados a clientes.
    """
    id_credito: Optional[int] = Field(None, description="ID único del crédito (AUTOINCREMENT)")
    ci_cliente: str = Field(..., description="CI del cliente con el crédito (clave foránea)")
    fecha_credito: date = Field(..., description="Fecha en que se otorgó el crédito")
    fecha_ultimo_abono: Optional[date] = Field(None, description="Fecha del último abono al crédito (opcional)")
    monto_total: float = Field(..., description="Monto total del crédito")
    monto_pagado: float = Field(..., description="Monto ya pagado del crédito")
    estado: str = Field(..., description="Estado del crédito ('Pagado', 'Pendiente', 'Parcial')")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode='json')

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Credito':
        return Credito(**data)

    def __repr__(self) -> str:
        return f"Credito(ID: {self.id_credito}, Cliente CI: {self.ci_cliente}, Estado: {self.estado})"

class Pago(BaseModel, PagoValidators):
    """
    Modelo para la tabla 'Pagos' .
    Registra los pagos asociados a una venta.
    """
    id_pago: Optional[int] = Field(None, description="ID único del pago (AUTOINCREMENT)")
    id_venta: int = Field(..., description="ID de la venta asociada al pago (clave foránea)")
    num_cor: str = Field(..., description="Número correlativo del pago")
    monto: float = Field(..., description="Monto del pago")
    fecha_pago: date = Field(..., description="Fecha en que se realizó el pago")
    metodo_pago: str = Field(..., description="Método de pago ('efectivo_bs', 'efectvo_usd', 'pago_movil', 'debito', 'transferencia')")
    referencia: Optional[str] = Field(None, description="Referencia del pago (ej. número de transferencia)")
    num_tefl: Optional[str] = Field(None, description="Número de teléfono asociado al pago móvil (opcional)")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode='json')

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Pago':
        return Pago(**data)

    def __repr__(self) -> str:
        return f"Pago(ID: {self.id_pago}, Venta ID: {self.id_venta}, Monto: {self.monto}, Método: {self.metodo_pago})"

class Inventario(BaseModel, InventarioValidators):
    """
    Modelo para la tabla 'Inventarios' .
    Registra los movimientos de inventario de un producto.
    """
    id_inventario: Optional[int] = Field(None, description="ID único del movimiento de inventario (AUTOINCREMENT)")
    cod_producto: str = Field(..., description="Código del producto afectado (clave foránea)")
    referencia: str = Field(..., description="Referencia del movimiento ('compra', 'venta', 'descarte', 'ajuste', 'traslado_tienda', 'autoconsumo')")
    comentario: Optional[str] = Field(None, description="Comentario adicional sobre el movimiento (opcional)")
    tipo_movimiento: str = Field(..., description="Tipo de movimiento ('entrada' o 'salida')")
    cant_movida: int = Field(..., description="Cantidad de producto movida")
    costo_unitario: Optional[float] = Field(..., description="Costo de compra del producto")
    id_compra: Optional[float] = Field(..., description="ID de la compra asociada al producto")
    fc_actualizacion: date = Field(..., description="Fecha de actualización del movimiento")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode='json')

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Inventario':
        return Inventario(**data)

    def __repr__(self) -> str:
        return f"Inventario(ID: {self.id_inventario}, Producto: {self.cod_producto}, Tipo: {self.tipo_movimiento}, Cant: {self.cant_movida})"

class DetalleVenta(BaseModel, DetalleVentaValidators):
    """
    Modelo para la tabla 'Detalle_Venta' .
    Detalle de los productos incluidos en una venta.
    """
    id_detalle: Optional[int] = Field(None, description="ID único del detalle de venta (AUTOINCREMENT)")
    id_venta: int = Field(..., description="ID de la venta a la que pertenece el detalle (clave foránea)")
    cod_producto: str = Field(..., description="Codigo del producto en el detalle (clave foránea)")
    cantidad_producto: int = Field(..., description="Cantidad del producto vendido")
    precio_unitario: float = Field(..., description="Precio unitario del producto al momento de la venta")

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DetalleVenta':
        return DetalleVenta(**data)

    def __repr__(self) -> str:
        return f"DetalleVenta(ID: {self.id_detalle}, Venta ID: {self.id_venta}, Producto: {self.cod_producto}, Cant: {self.cantidad_producto})"


    """
    Clase para gestionar la conexión a la base de datos SQLite
    y la creación de las tablas.
    """
    def __init__(self, db_path: str = 'cafetin_management.db'):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def connect(self):
        """Establece la conexión a la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row # Para acceder a las columnas por nombre
            self.cursor = self.conn.cursor()
            print(f"Conectado a la base de datos: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conn = None
            self.cursor = None

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")
            self.conn = None
            self.cursor = None
