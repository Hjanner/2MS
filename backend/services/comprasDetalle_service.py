import sqlite3
from typing import List, Optional, Dict
from datetime import date
from backend.models.view_models import DetalleCompra, DetalleProductoCompra, ResumenCompra
from backend.models.models import Compra, Proveedor, Producto, ProductoNoPreparado, Movimiento

class CompraService:
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

    def obtener_detalle_compra(self, id_compra: int) -> Optional[DetalleCompra]:
        """
        Obtiene el detalle completo de una compra utilizando la vista SQL vista_detalle_compras
        y construye el modelo Pydantic completo.
        """
        # 1. Obtener datos básicos de la compra
        compra_data = self._get_single_record(
            "SELECT * FROM Compras WHERE id_compra = ?", 
            (id_compra,)
        )
        if not compra_data:
            return None

        # 2. Obtener datos del proveedor
        proveedor_data = self._get_single_record(
            "SELECT * FROM Proveedores WHERE Rif = ?",
            (compra_data['Rif'],)
        )
        if not proveedor_data:
            raise ValueError(f"Proveedor con RIF {compra_data['Rif']} no encontrado")

        # 3. Obtener productos de la compra desde la vista
        productos_data = self._execute_query(
            """
            SELECT 
                cod_producto,
                nombre_producto,
                imagen_producto,
                stock_minimo,
                stock_actual,
                unidad_medida,
                cantidad_comprada,
                costo_unitario_compra,
                subtotal,
                comentario_movimiento
            FROM vista_detalle_compras
            WHERE id_compra = ?
            """,
            (id_compra,)
        )

        # 4. Construir los modelos Pydantic
        compra = Compra(**compra_data)
        proveedor = Proveedor(**proveedor_data)
        
        productos = []
        for p in productos_data:
            # Construir modelo Producto
            producto = Producto(
                cod_producto=p['cod_producto'],
                nombre=p['nombre_producto'],
                img=p['imagen_producto'],
                # Campos no incluidos en la vista se dejan con valores por defecto
                precio_usd=0.1,
                id_categoria=None
            )
            
            # Construir modelo ProductoNoPreparado
            producto_no_prep = ProductoNoPreparado(
                cod_producto_noPreparado=p['cod_producto'],
                cant_min=p['stock_minimo'],
                cant_actual=p['stock_actual'],
                costo_compra=p['costo_unitario_compra'],
                unidad_medida=p['unidad_medida'],
                Rif=compra.Rif  # Usamos el RIF de la compra
            )
            
            # Construir modelo Movimiento
            movimiento = Movimiento(
                cod_producto=p['cod_producto'],
                referencia='compra',
                comentario=p['comentario_movimiento'],
                tipo_movimiento='entrada',
                cant_movida=p['cantidad_comprada'],
                costo_unitario=p['costo_unitario_compra'],
                id_compra=id_compra,
                fc_actualizacion=compra.fecha  # Usamos la fecha de la compra
            )
            
            productos.append(DetalleProductoCompra(
                producto=producto,
                producto_no_preparado=producto_no_prep,
                movimiento=movimiento
            ))

        # 5. Formatear fecha y retornar el modelo completo
        return DetalleCompra(
            compra=compra,
            proveedor=proveedor,
            productos=productos,
            fecha_formateada=compra.fecha.strftime("%d/%m/%Y")
        )

    def obtener_resumenes_compras(
        self,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        rif_proveedor: Optional[str] = None,
        limit: int = 100
    ) -> List[ResumenCompra]:
        """
        Obtiene resúmenes de compras con filtros opcionales.
        Utiliza la vista para contar eficientemente los productos por compra.
        """
        # 1. Construir consulta base con filtros
        query = """
            SELECT 
                c.*,
                (SELECT COUNT(*) FROM vista_detalle_compras v WHERE v.id_compra = c.id_compra) as cantidad_productos
            FROM Compras c
        """
        conditions = []
        params = []
        
        if fecha_inicio:
            conditions.append("c.fecha >= ?")
            params.append(fecha_inicio)
        if fecha_fin:
            conditions.append("c.fecha <= ?")
            params.append(fecha_fin)
        if rif_proveedor:
            conditions.append("c.Rif = ?")
            params.append(rif_proveedor)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY c.fecha DESC LIMIT ?"
        params.append(limit)
        
        # 2. Ejecutar consulta
        compras_data = self._execute_query(query, params)
        
        # 3. Procesar resultados
        resumenes = []
        for c in compras_data:
            # Obtener proveedor
            proveedor_data = self._get_single_record(
                "SELECT * FROM Proveedores WHERE Rif = ?",
                (c['Rif'],)
            )
            if not proveedor_data:
                continue  # Saltar compras sin proveedor válido
            
            # Construir modelos
            compra = Compra(**c)
            proveedor = Proveedor(**proveedor_data)
            
            resumenes.append(ResumenCompra(
                compra=compra,
                proveedor=proveedor,
                cantidad_productos=c['cantidad_productos'],
                fecha_formateada=compra.fecha.strftime("%d/%m/%Y")
            ))
        
        return resumenes