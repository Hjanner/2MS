import sqlite3
from typing import List
from fastapi import HTTPException
from backend.models.models import DetalleVenta, Pago, Venta, ProductoNoPreparado

def registrar_venta_con_detalles_y_pago(
    venta_data: Venta,
    detalles_data: List[DetalleVenta],
    pago_data: Pago,
    db_path: str
) -> dict:
    """
    Registra una venta completa con sus detalles y pago asociado,
    validando que no queden cantidades negativas en inventario.
    
    Args:
        venta_data: Datos de la venta
        detalles_data: Lista de detalles de productos vendidos
        pago_data: Datos del pago asociado
        db_path: Ruta a la base de datos SQLite
    
    Returns:
        dict: Resultado de la operación con ID de venta generado
        
    Raises:
        HTTPException: Si hay errores de validación o en la transacción
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # # 1. Validaciones iniciales
        # total_detalles = sum(d.precio_unitario * d.cantidad_producto for d in detalles_data)
        # if abs(total_detalles - venta_data.monto_total_bs) > 0.01:
        #     raise ValueError("El monto total no coincide con la suma de los productos")
        
        if abs(pago_data.monto - venta_data.monto_total_bs) > 0.01:
            raise ValueError("El monto del pago no coincide con el total de la venta")

        # 2. Verificar stock antes de comenzar la transacción
        productos_verificar = {}
        for detalle in detalles_data:
            cursor.execute(
                """SELECT p.cod_producto, np.cant_actual
                   FROM Productos p
                   LEFT JOIN Productos_noPreparados np ON p.cod_producto = np.cod_producto_noPreparado
                   WHERE p.cod_producto = ?""",
                (detalle.cod_producto,)
            )
            producto = cursor.fetchone()
            
            if not producto:
                raise ValueError(f"Producto {detalle.cod_producto} no encontrado")
            
            cod_producto, cant_actual = producto
            
            # Solo verificamos stock para productos no preparados
            if cant_actual is not None:
                nueva_cantidad = cant_actual - detalle.cantidad_producto
                if nueva_cantidad < 0:
                    raise ValueError(
                        f"No hay suficiente stock para {cod_producto}. "
                        f"Stock actual: {cant_actual}, solicitado: {detalle.cantidad_producto}"
                    )
                productos_verificar[cod_producto] = {
                    'cant_actual': cant_actual,
                    'nueva_cantidad': nueva_cantidad
                }

        # 3. Iniciar transacción
        cursor.execute("BEGIN TRANSACTION")

        # 4. Insertar la venta
        cursor.execute(
            """INSERT INTO Ventas (
                monto_total_bs, fecha_hora, monto_total_usd, 
                tipo, ci_cliente, id_tasa
            ) VALUES (?, ?, ?, ?, ?, ?)""",
            (
                venta_data.monto_total_bs,
                venta_data.fecha_hora,
                venta_data.monto_total_usd,
                venta_data.tipo,
                venta_data.ci_cliente,
                venta_data.id_tasa
            )
        )
        id_venta = cursor.lastrowid

        # 5. Insertar detalles
        for detalle in detalles_data:
            # Insertar detalle
            cursor.execute(
                """INSERT INTO Detalle_Venta (
                    id_venta, cod_producto, cantidad_producto, precio_unitario
                ) VALUES (?, ?, ?, ?)""",
                (
                    id_venta,
                    detalle.cod_producto,
                    detalle.cantidad_producto,
                    detalle.precio_unitario
                )
            )
            
        # 6. Insertar el pago
        cursor.execute(
            """INSERT INTO Pagos (
                id_venta, monto, fecha_pago, 
                metodo_pago, referencia, num_tefl
            ) VALUES (?, ?, ?, ?, ?, ?)""",
            (
                id_venta,
                pago_data.monto,
                pago_data.fecha_pago,
                pago_data.metodo_pago,
                pago_data.referencia or None,
                pago_data.num_tefl or None
            )
        )

        # 7. Confirmar transacción
        conn.commit()
        
        return {
            "success": True,
            "message": "Venta registrada exitosamente",
            "id_venta": id_venta,
            "productos_actualizados": productos_verificar
        }

    except ValueError as ve:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=422,
            detail={
                "success": False,
                "error": "Error de validación",
                "message": str(ve)
            }
        )
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "error": "Error en la transacción",
                "message": str(e)
            }
        )
    finally:
        if conn:
            conn.close()