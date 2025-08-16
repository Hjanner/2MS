import sqlite3
from database import db_path

PRODUCTOS_COMPLETOS_VIEW = """
CREATE VIEW vista_productos_completos AS
SELECT 
  p.*,
  c.descr as categoria_descr,
  c.tipo as categoria_tipo,
  np.cant_min, np.cant_actual, np.costo_compra, np.unidad_medida, np.Rif,
  pp.descr as descr_preparado,
  CASE 
    WHEN np.cod_producto_noPreparado IS NOT NULL THEN 'noPreparado'
    WHEN pp.cod_producto_preparado IS NOT NULL THEN 'preparado'
    ELSE 'sin_tipo'
  END as tipo_producto
FROM Productos p
LEFT JOIN categoria_productos c ON p.id_categoria = c.id_categoria
LEFT JOIN Productos_noPreparados np ON p.cod_producto = np.cod_producto_noPreparado
LEFT JOIN Productos_preparados pp ON p.cod_producto = pp.cod_producto_preparado;
"""

COMPRAS_DETALLES_VIEW = """
CREATE VIEW vista_detalle_compras AS
SELECT 
    c.id_compra,
    c.fecha AS fecha_compra,
    c.gasto_total,
    
    -- Información del proveedor
    p.Rif AS rif_proveedor,
    p.razon_social AS nombre_proveedor,
    
    -- Información del producto
    pr.cod_producto,
    pr.nombre AS nombre_producto,
    pr.img AS imagen_producto,
    
    -- Información específica del producto no preparado
    np.cant_min AS stock_minimo,
    np.cant_actual AS stock_actual,
    np.unidad_medida,
    
    -- Detalles del movimiento/compra
    m.cant_movida AS cantidad_comprada,
    m.costo_unitario AS costo_unitario_compra,
    (m.cant_movida * m.costo_unitario) AS subtotal,
    m.comentario AS comentario_movimiento,
    m.fc_actualizacion AS fecha_actualizacion_movimiento
    
FROM 
    Compras c
JOIN 
    Proveedores p ON c.Rif = p.Rif
JOIN 
    Movimientos m ON c.id_compra = m.id_compra
JOIN 
    Productos pr ON m.cod_producto = pr.cod_producto
JOIN 
    Productos_noPreparados np ON pr.cod_producto = np.cod_producto_noPreparado
WHERE 
    m.referencia = 'compra'
ORDER BY 
    c.fecha DESC, c.id_compra DESC, pr.nombre;
"""

#-- Vista para el detalle completo de una venta (DetalleVentaCompleto)
VENTAS_DETALLES_VIEW = """
CREATE VIEW vista_detalle_venta_completo AS
SELECT 
    v.id_venta,
    v.monto_total_bs,
    v.monto_total_usd,
    strftime('%d/%m/%Y', v.fecha_hora) AS fecha_formateada,
    strftime('%H:%M', v.fecha_hora) AS hora_formateada,
    v.tipo,
    v.ci_cliente,
    c.nombre AS nombre_cliente,
    c.tlf AS telefono_cliente,
    p.id_pago,
    p.monto AS monto_pago,
    p.metodo_pago,
    p.referencia,
    tc.valor_usd_bs AS tasa_cambio,
    COUNT(dv.id_detalle) AS cantidad_productos_diferentes,
    SUM(dv.cantidad_producto) AS cantidad_total_productos
FROM 
    Ventas v
LEFT JOIN 
    Clientes c ON v.ci_cliente = c.ci_cliente
LEFT JOIN 
    Pagos p ON v.id_venta = p.id_venta
LEFT JOIN 
    TasasCambio tc ON v.id_tasa = tc.id_tasa
LEFT JOIN 
    Detalle_Venta dv ON v.id_venta = dv.id_venta
GROUP BY 
    v.id_venta;
"""

#-- Vista para los productos de una venta (DetalleProductoVenta)
VENTA_PRODUCTO_DETALLE_VIEW = """
CREATE VIEW vista_detalle_productos_venta AS
SELECT 
    dv.id_venta,
    dv.id_detalle,
    dv.cod_producto,
    p.nombre AS nombre_producto,
    dv.cantidad_producto,
    dv.precio_unitario,
    (dv.cantidad_producto * dv.precio_unitario) AS subtotal,
    p.id_categoria
FROM 
    Detalle_Venta dv
JOIN 
    Productos p ON dv.cod_producto = p.cod_producto;
"""

#-- Vista para resumen de ventas (ResumenVenta) se usa para listar
VENTA_RESUMEN_VIEW = """
-- Vista para resumen de ventas (ResumenVenta)
CREATE VIEW vista_resumen_ventas AS
SELECT 
    v.id_venta,
    strftime('%d/%m/%Y', v.fecha_hora) AS fecha_formateada,
    strftime('%H:%M', v.fecha_hora) AS hora_formateada,
    v.monto_total_usd,
    v.monto_total_bs,
    v.tipo,
    v.ci_cliente,
    c.nombre AS nombre_cliente,
    p.metodo_pago,
    p.monto AS monto_pago,
    COUNT(dv.id_detalle) AS productos_diferentes,
    SUM(dv.cantidad_producto) AS cantidad_total_productos,
    tc.valor_usd_bs AS tasa_cambio
FROM 
    Ventas v
LEFT JOIN 
    Clientes c ON v.ci_cliente = c.ci_cliente
LEFT JOIN 
    Pagos p ON v.id_venta = p.id_venta
LEFT JOIN 
    Detalle_Venta dv ON v.id_venta = dv.id_venta
LEFT JOIN 
    TasasCambio tc ON v.id_tasa = tc.id_tasa
GROUP BY 
    v.id_venta;
"""

ALL_VIEWS = [
    PRODUCTOS_COMPLETOS_VIEW,
    COMPRAS_DETALLES_VIEW,
    VENTAS_DETALLES_VIEW,
    VENTA_PRODUCTO_DETALLE_VIEW,
    VENTA_RESUMEN_VIEW
]

print("Creando Views en:", db_path)

def create_views():
    conn = None 
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for view in ALL_VIEWS:
            cursor.execute(view)
        conn.commit()
        print("Views creado correctamente.")

        
    except sqlite3.Error as e:
        print(f"Ha ocurido un error creando las Views: {e}")
        if conn:
            conn.rollback() 
    finally:
        if conn:
            conn.close()
            
if __name__ == "__main__":
    create_views()