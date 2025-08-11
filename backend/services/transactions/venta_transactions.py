import sqlite3
from typing import Dict, List

def registrar_venta_con_detalles_y_pago(
        venta_data: Dict, 
        detalles_data: List[Dict], 
        pago_data: Dict, 
        db_path: str
    ) -> int:
    """
    Registra una venta completa con sus detalles y pago como transacción atómica.
    
    Args:
        venta_data: Diccionario con datos de la venta {
            'monto_total_bs': float,
            'fecha_hora': str (formato ISO),
            'monto_total_usd': float,
            'tipo': str,
            'ci_cliente': str,
            'id_tasa': int
        }
        detalles_data: Lista de diccionarios con detalles de productos [{
            'cod_producto': str,
            'cantidad_producto': int,
            'precio_unitario': float
        }]
        pago_data: Diccionario con datos del pago {
            'monto': float,
            'fecha_pago': str (formato ISO),
            'metodo_pago': str,
            'referencia': str,
            'num_tefl': str
        }
        db_path: Ruta al archivo de base de datos
    
    Returns:
        int: ID de la venta registrada
    
    Raises:
        sqlite3.Error: Si ocurre algún error en la base de datos
        ValueError: Si hay inconsistencias en los datos
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Validación básica de datos
        if abs(sum(d['precio_unitario'] * d['cantidad_producto'] for d in detalles_data) - venta_data['monto_total_bs']) > 0.01:
            raise ValueError("El monto total no coincide con la suma de los productos")
        
        if abs(pago_data['monto'] - venta_data['monto_total_bs']) > 0.01:
            raise ValueError("El monto del pago no coincide con el total de la venta")
        
        # Iniciar transacción
        cursor.execute("BEGIN TRANSACTION")
        
        # 1. Insertar la venta
        cursor.execute(
            """INSERT INTO Ventas (
                monto_total_bs, fecha_hora, monto_total_usd, 
                tipo, ci_cliente, id_tasa
            ) VALUES (?, ?, ?, ?, ?, ?)""",
            (
                venta_data['monto_total_bs'],
                venta_data['fecha_hora'],
                venta_data['monto_total_usd'],
                venta_data['tipo'],
                venta_data['ci_cliente'],
                venta_data['id_tasa']
            )
        )
        id_venta = cursor.lastrowid
        
        # 2. Insertar los detalles de venta
        for detalle in detalles_data:
            # Verificar existencia del producto
            cursor.execute(
                "SELECT 1 FROM Productos WHERE cod_producto = ?",
                (detalle['cod_producto'],)
            )
            if not cursor.fetchone():
                raise ValueError(f"Producto {detalle['cod_producto']} no existe")
            
            cursor.execute(
                """INSERT INTO Detalle_Venta (
                    id_venta, cod_producto, cantidad_producto, precio_unitario
                ) VALUES (?, ?, ?, ?)""",
                (
                    id_venta,
                    detalle['cod_producto'],
                    detalle['cantidad_producto'],
                    detalle['precio_unitario']
                )
            )
        
        # 3. Insertar el pago
        cursor.execute(
            """INSERT INTO Pagos (
                id_venta, monto, fecha_pago, 
                metodo_pago, referencia, num_tefl
            ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                id_venta,
                pago_data['monto'],
                pago_data['fecha_pago'],
                pago_data['metodo_pago'],
                pago_data.get('referencia', ''),
                pago_data.get('num_tefl', '')
            )
        )
        
        # 4. Confirmar transacción (el trigger se encargará de los movimientos)
        conn.commit()
        return id_venta
        
    except Exception as e:
        if conn:
            conn.rollback()
        raise  # Re-lanzar la excepción para manejo superior
    finally:
        if conn:
            conn.close()