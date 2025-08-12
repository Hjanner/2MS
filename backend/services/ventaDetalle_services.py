import sqlite3
from typing import List, Optional, Dict
from datetime import datetime
from backend.models.view_models import DetalleVentaCompleto, DetalleProductoVenta, ResumenVenta
from backend.models.models import Venta, Cliente, ProductoBase, DetalleVenta, Pago, TasaCambio

class VentaDetalleService:
    def __init__(self, db_path: str = None):
        self.db_path = db_path

    def _execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Ejecuta una consulta y devuelve los resultados como diccionarios"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def _get_single_record(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Obtiene un único registro de la base de datos"""
        results = self._execute_query(query, params)
        return results[0] if results else None

    def obtener_detalle_venta(self, id_venta: int) -> Optional[DetalleVentaCompleto]:
        """
        Obtiene el detalle completo de una venta utilizando las vistas SQL
        y construye el modelo Pydantic completo.
        """
        # 1. Obtener datos básicos de la venta desde la vista
        venta_data = self._get_single_record(
            "SELECT * FROM vista_detalle_venta_completo WHERE id_venta = ?", 
            (id_venta,)
        )
        if not venta_data:
            return None

        # 2. Obtener datos del cliente si existe
        cliente = None
        if venta_data.get('ci_cliente'):
            cliente_data = self._get_single_record(
                "SELECT * FROM Clientes WHERE ci = ?",
                (venta_data['ci_cliente'],)
            )
            if cliente_data:
                cliente = Cliente(**cliente_data)

        # 3. Obtener datos del pago
        pago_data = self._get_single_record(
            "SELECT * FROM Pagos WHERE id_venta = ?",
            (id_venta,)
        )
        if not pago_data:
            raise ValueError(f"No se encontró pago para la venta {id_venta}")
        pago = Pago(**pago_data)

        # 4. Obtener datos de la tasa de cambio si existe
        tasa_cambio = None
        if venta_data.get('tasa_cambio'):
            tasa_data = self._get_single_record(
                "SELECT * FROM TasasCambio WHERE valor_usd_bs = ? AND fecha <= ? ORDER BY fecha DESC LIMIT 1",
                (venta_data['tasa_cambio'], venta_data['fecha_formateada'])
            )
            if tasa_data:
                tasa_cambio = TasaCambio(**tasa_data)

        # 5. Obtener productos de la venta desde la vista
        productos_data = self._execute_query(
            "SELECT * FROM vista_detalle_productos_venta WHERE id_venta = ?",
            (id_venta,)
        )

        # 6. Construir los modelos Pydantic para los productos
        productos = []
        for p in productos_data:
            # Construir modelo ProductoBase
            producto = ProductoBase(
                cod_producto=p['cod_producto'],
                nombre=p['nombre_producto'],
                precio_usd=p['precio_unitario'],  # Asumimos que el precio unitario es en USD
                id_categoria=p.get('id_categoria')
            )
            
            # Construir modelo DetalleVenta
            detalle_venta = DetalleVenta(
                id_detalle=p['id_detalle'],
                id_venta=id_venta,
                cod_producto=p['cod_producto'],
                cantidad_producto=p['cantidad_producto'],
                precio_unitario=p['precio_unitario']
            )
            
            productos.append(DetalleProductoVenta(
                producto=producto,
                detalle_venta=detalle_venta
            ))

        # 7. Construir modelo Venta
        venta = Venta(
            id_venta=venta_data['id_venta'],
            monto_total_bs=venta_data['monto_total_bs'],
            monto_total_usd=venta_data['monto_total_usd'],
            fecha_hora=datetime.strptime(f"{venta_data['fecha_formateada']} {venta_data['hora_formateada']}", "%d/%m/%Y %H:%M"),
            tipo=venta_data['tipo'],
            ci_cliente=venta_data.get('ci_cliente'),
            id_tasa=tasa_cambio.id_tasa if tasa_cambio else None
        )

        # 8. Retornar el modelo completo
        return DetalleVentaCompleto(
            venta=venta,
            cliente=cliente,
            productos=productos,
            pago=pago,
            tasa_cambio=tasa_cambio,
            fecha_formateada=venta_data['fecha_formateada'],
            hora_formateada=venta_data['hora_formateada']
        )

    def obtener_resumenes_ventas(
        self,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        ci_cliente: Optional[str] = None,
        tipo_venta: Optional[str] = None,
        metodo_pago: Optional[str] = None,
        limit: int = 100
    ) -> List[ResumenVenta]:
        """
        Obtiene resúmenes de ventas con filtros opcionales.
        Utiliza la vista vista_resumen_ventas para mayor eficiencia.
        """
        # 1. Construir consulta base con filtros
        query = "SELECT * FROM vista_resumen_ventas"
        conditions = []
        params = []
        
        if fecha_inicio:
            conditions.append("fecha_formateada >= ?")
            params.append(fecha_inicio)
        if fecha_fin:
            conditions.append("fecha_formateada <= ?")
            params.append(fecha_fin)
        if ci_cliente:
            conditions.append("ci_cliente = ?")
            params.append(ci_cliente)
        if tipo_venta:
            conditions.append("tipo = ?")
            params.append(tipo_venta)
        if metodo_pago:
            conditions.append("metodo_pago = ?")
            params.append(metodo_pago)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY fecha_formateada DESC, hora_formateada DESC LIMIT ?"
        params.append(limit)
        
        # 2. Ejecutar consulta
        ventas_data = self._execute_query(query, params)
        
        # 3. Procesar resultados
        resumenes = []
        for v in ventas_data:
            # Obtener cliente si existe
            cliente = None
            if v.get('ci_cliente'):
                cliente_data = self._get_single_record(
                    "SELECT * FROM Clientes WHERE ci = ?",
                    (v['ci_cliente'],)
                )
                if cliente_data:
                    cliente = Cliente(**cliente_data)
            
            # Obtener pago
            pago_data = self._get_single_record(
                "SELECT * FROM Pagos WHERE id_venta = ?",
                (v['id_venta'],)
            )
            if not pago_data:
                continue  # Saltar ventas sin pago
            pago = Pago(**pago_data)
            
            # Construir modelo Venta
            venta = Venta(
                id_venta=v['id_venta'],
                monto_total_bs=v['monto_total_bs'],
                monto_total_usd=v['monto_total_usd'],
                fecha_hora=datetime.strptime(f"{v['fecha_formateada']} {v['hora_formateada']}", "%d/%m/%Y %H:%M"),
                tipo=v['tipo'],
                ci_cliente=v.get('ci_cliente'),
                id_tasa=None  # No incluido en el resumen
            )
            
            resumenes.append(ResumenVenta(
                venta=venta,
                cliente=cliente,
                cantidad_productos=v['cantidad_total_productos'],
                pago=pago,
                fecha_formateada=v['fecha_formateada'],
                hora_formateada=v['hora_formateada']
            ))
        
        return resumenes

    def obtener_ventas_por_producto(
        self, 
        cod_producto: str,
        fecha_inicio: Optional[str] = None,
        fecha_fin: Optional[str] = None,
        limit: int = 100
    ) -> List[DetalleProductoVenta]:
        """
        Obtiene todas las ventas donde aparece un producto específico
        """
        query = """
            SELECT v.*, dv.*, p.nombre as nombre_producto
            FROM vista_detalle_productos_venta v
            JOIN Productos p ON v.cod_producto = p.cod_producto
            WHERE v.cod_producto = ?
        """
        params = [cod_producto]
        
        if fecha_inicio:
            query += " AND v.fecha_formateada >= ?"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND v.fecha_formateada <= ?"
            params.append(fecha_fin)
        
        query += " ORDER BY v.fecha_formateada DESC, v.hora_formateada DESC LIMIT ?"
        params.append(limit)
        
        productos_data = self._execute_query(query, params)
        
        productos = []
        for p in productos_data:
            producto = ProductoBase(
                cod_producto=p['cod_producto'],
                nombre=p['nombre_producto'],
                precio_usd=p['precio_unitario'],
                id_categoria=p.get('id_categoria')
            )
            
            detalle_venta = DetalleVenta(
                id_detalle=p['id_detalle'],
                id_venta=p['id_venta'],
                cod_producto=p['cod_producto'],
                cantidad_producto=p['cantidad_producto'],
                precio_unitario=p['precio_unitario']
            )
            
            productos.append(DetalleProductoVenta(
                producto=producto,
                detalle_venta=detalle_venta
            ))
        
        return productos