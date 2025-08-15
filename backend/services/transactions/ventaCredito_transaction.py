import sqlite3
from typing import List, Optional
from fastapi import HTTPException
from backend.models.models import DetalleVenta, Pago, Venta, Credito
from backend.services.transactions.venta_transactions import registrar_venta_con_detalles_y_pago

def registrar_venta_credito_completa(
    venta_data: Venta,
    detalles_data: List[DetalleVenta],
    credito_data: Credito,
    db_path: str,
    pago_inicial: Optional[Pago] = None
) -> dict:
    """
    Registra una venta a crédito completa con sus detalles, registro de crédito
    y pago inicial opcional.
    
    Args:
        venta_data: Datos de la venta
        detalles_data: Lista de detalles de productos vendidos
        credito_data: Datos del crédito a crear
        pago_inicial: Pago inicial opcional (puede ser None si no hay pago inicial)
        db_path: Ruta a la base de datos SQLite
    
    Returns:
        dict: Resultado de la operación con IDs generados
        
    Raises:
        HTTPException: Si hay errores de validación o en la transacción
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Validaciones iniciales
        if venta_data.tipo != 'credito':
            raise ValueError("El tipo de venta debe ser 'credito'")
            
        if not venta_data.ci_cliente:
            raise ValueError("Las ventas a crédito requieren un cliente")
            
        if venta_data.ci_cliente != credito_data.ci_cliente:
            raise ValueError("El cliente de la venta debe coincidir con el del crédito")
        
        # Validar que el cliente existe
        cursor.execute("SELECT ci_cliente FROM Clientes WHERE ci_cliente = ?", (venta_data.ci_cliente,))
        if not cursor.fetchone():
            raise ValueError(f"Cliente {venta_data.ci_cliente} no encontrado")
        
        # Validar montos del crédito
        if credito_data.monto_total != venta_data.monto_total_usd:
            raise ValueError("El monto total del crédito debe coincidir con el monto USD de la venta")
            
        if pago_inicial:
            if pago_inicial.monto > venta_data.monto_total_bs:
                raise ValueError("El pago inicial no puede ser mayor al total de la venta")
            
            # Convertir pago inicial a USD para comparar con crédito
            pago_inicial_usd = pago_inicial.monto / (venta_data.monto_total_bs / venta_data.monto_total_usd)
            # print('credito_data.monto_pagado', credito_data.monto_pagado)
            # print('pago_inicial_usd', pago_inicial_usd)

            # if credito_data.monto_pagado != pago_inicial_usd:
            #     raise ValueError("El monto pagado del crédito debe coincidir con el pago inicial en USD")

        # 2. Verificar stock para productos no preparados
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

        # 5. Insertar detalles de venta
        for detalle in detalles_data:
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

        # 6. Insertar el crédito
        cursor.execute(
            """INSERT INTO Creditos (
                ci_cliente, fecha_credito, fecha_ultimo_abono,
                monto_total, monto_pagado, estado, id_venta
            ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                credito_data.ci_cliente,
                credito_data.fecha_credito,
                credito_data.fecha_ultimo_abono,
                credito_data.monto_total,
                credito_data.monto_pagado,
                credito_data.estado,
                id_venta,
            )
        )
        id_credito = cursor.lastrowid

        # 7. Insertar pago inicial si existe
        id_pago = None
        if pago_inicial:
            cursor.execute(
                """INSERT INTO Pagos (
                    id_venta, monto, fecha_pago, 
                    metodo_pago, referencia, num_tefl
                ) VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    id_venta,
                    pago_inicial.monto,
                    pago_inicial.fecha_pago,
                    pago_inicial.metodo_pago,
                    pago_inicial.referencia or None,
                    pago_inicial.num_tefl or None
                )
            )
            id_pago = cursor.lastrowid

        # 8. Actualizar inventario para productos no preparados
        for cod_producto, info in productos_verificar.items():
            cursor.execute(
                """UPDATE Productos_noPreparados 
                   SET cant_actual = ? 
                   WHERE cod_producto_noPreparado = ?""",
                (info['nueva_cantidad'], cod_producto)
            )

        # 9. Confirmar transacción
        conn.commit()
        
        result = {
            "success": True,
            "message": "Venta a crédito registrada exitosamente",
            "id_venta": id_venta,
            "id_credito": id_credito,
            "productos_actualizados": productos_verificar
        }
        
        if id_pago:
            result["id_pago_inicial"] = id_pago
            
        return result

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


def registrar_venta_completa(
    venta_data: Venta,
    detalles_data: List[DetalleVenta],
    db_path: str,
    pago_data: Optional[Pago] = None,
    credito_data: Optional[Credito] = None,
    
) -> dict:
    """
    Función unificada que maneja tanto ventas de contado como a crédito.
    
    Args:
        venta_data: Datos de la venta
        detalles_data: Lista de detalles de productos vendidos
        pago_data: Datos del pago (obligatorio para venta de contado, opcional para crédito)
        credito_data: Datos del crédito (solo para ventas a crédito)
        db_path: Ruta a la base de datos SQLite
    
    Returns:
        dict: Resultado de la operación
    """
    if venta_data.tipo == 'credito':
        if not credito_data:
            raise HTTPException(
                status_code=422,
                detail={
                    "success": False,
                    "error": "Error de validación",
                    "message": "Las ventas a crédito requieren datos del crédito"
                }
            )
        return registrar_venta_credito_completa(
            venta_data=venta_data,
            detalles_data=detalles_data,
            credito_data=credito_data,
            pago_inicial=pago_data,
            db_path=db_path
        )
    else:
        if not pago_data:
            raise HTTPException(
                status_code=422,
                detail={
                    "success": False,
                    "error": "Error de validación",
                    "message": "Las ventas de contado requieren datos del pago"
                }
            )
        return registrar_venta_con_detalles_y_pago(
            venta_data=venta_data,
            detalles_data=detalles_data,
            pago_data=pago_data,
            db_path=db_path
        )