import sqlite3
from database import db_path

#actualiza el stock de productos, despues del cambio en la tabla de movimientos a causa de una compra
MOVIMIENTO_COMPRA_TRIGGER_BEFORE = """
CREATE TRIGGER IF NOT EXISTS tr_after_movimiento_insert
AFTER INSERT ON Movimientos
WHEN NEW.referencia = 'compra'
BEGIN
    -- Validar que tenga costo_unitario para compras
    SELECT CASE
        WHEN NEW.costo_unitario IS NULL
        THEN RAISE(ABORT, 'Las compras deben especificar costo_unitario')
    END;
    
    -- Actualizar stock solo para productos no preparados
    UPDATE Productos_noPreparados
    SET cant_actual = cant_actual + NEW.cant_movida
    WHERE cod_producto_noPreparado = NEW.cod_producto;
END;
"""

#actualiza la tabla movimiento, al momento de crear uno producto no preparado
INGRESAR_NOPREPARADO_TRIGGER = """
CREATE TRIGGER IF NOT EXISTS tr_after_producto_nopreparado_insert
AFTER INSERT ON Productos_noPreparados
BEGIN
    -- Verificar que el producto exista en la tabla Productos
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM Productos WHERE cod_producto = NEW.cod_producto_noPreparado) = 0
        THEN RAISE(ABORT, 'El producto no existe en la tabla Productos')
    END;
    
    -- Insertar movimiento de inventario inicial (entrada por ajuste inicial)
    INSERT INTO Movimientos (
        cod_producto,
        referencia,
        tipo_movimiento,
        cant_movida,
        costo_unitario,
        fc_actualizacion,
        comentario
    ) VALUES (
        NEW.cod_producto_noPreparado,
        'ajuste',
        'entrada',
        NEW.cant_actual,
        NEW.costo_compra,
        date('now'),
        'Registro inicial de producto no preparado'
    );
END;
"""

#actualiza Productos_noPreparados si detecta un cambio en la cantidad actual
ACTUALIZAR_NOPREPARADO_TRIGGER = """
CREATE TRIGGER IF NOT EXISTS tr_after_producto_nopreparado_update
AFTER UPDATE OF cant_actual ON Productos_noPreparados
WHEN NEW.cant_actual <> OLD.cant_actual
BEGIN
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM Movimientos 
        WHERE cod_producto = NEW.cod_producto_noPreparado 
          AND referencia = 'compra' 
          AND fc_actualizacion >= datetime('now', '-5 seconds')
    ) THEN RAISE(IGNORE) END;

    
    INSERT INTO Movimientos (
        cod_producto,
        referencia,
        tipo_movimiento,
        cant_movida,
        costo_unitario,
        fc_actualizacion,
        comentario
    ) VALUES (
        NEW.cod_producto_noPreparado,
        'ajuste',
        CASE WHEN NEW.cant_actual > OLD.cant_actual THEN 'entrada' ELSE 'salida' END,
        abs(NEW.cant_actual - OLD.cant_actual),
        NEW.costo_compra,
        date('now'),
        'Ajuste de inventario'
    );
END;
"""

VENTA_COMPLETA_TRIGGER = """
-- Trigger para actualizar inventario después de venta
CREATE TRIGGER IF NOT EXISTS tr_after_venta_completa
AFTER INSERT ON Pagos
WHEN (SELECT COUNT(*) FROM Ventas WHERE id_venta = NEW.id_venta) > 0
BEGIN
    -- Registrar movimientos de salida por cada producto vendido
    INSERT INTO Movimientos (
        cod_producto, 
        referencia, 
        tipo_movimiento, 
        cant_movida, 
        fc_actualizacion,
        comentario
    )
    SELECT 
        dv.cod_producto,
        'venta',
        'salida',
        dv.cantidad_producto,
        datetime('now'),
        'Venta #' || NEW.id_venta
    FROM Detalle_Venta dv
    WHERE dv.id_venta = NEW.id_venta;
    
    -- Actualizar stock de productos no preparados
    UPDATE Productos_noPreparados
    SET cant_actual = cant_actual - (
        SELECT SUM(dv.cantidad_producto)
        FROM Detalle_Venta dv
        WHERE dv.cod_producto = Productos_noPreparados.cod_producto_noPreparado
        AND dv.id_venta = NEW.id_venta
    )
    WHERE cod_producto_noPreparado IN (
        SELECT cod_producto FROM Detalle_Venta WHERE id_venta = NEW.id_venta
    );
END;
"""

#Se activa después de cualquier INSERT en la tabla Movimientos, excepto para compras, Actualiza el stock en Productos_noPreparados
MOVIMIENTO_GENERAL_TRIGGER = """
CREATE TRIGGER IF NOT EXISTS tr_after_movimiento_general_insert
AFTER INSERT ON Movimientos
WHEN NEW.referencia NOT IN ('compra') -- Excluir compras porque ya tienen su propio trigger
BEGIN
    -- Validar que el producto sea no preparado antes de actualizar stock
    UPDATE Productos_noPreparados
    SET cant_actual = CASE 
        WHEN NEW.tipo_movimiento = 'entrada' THEN cant_actual + NEW.cant_movida
        WHEN NEW.tipo_movimiento = 'salida' THEN cant_actual - NEW.cant_movida
        ELSE cant_actual
    END
    WHERE cod_producto_noPreparado = NEW.cod_producto
    AND EXISTS (
        SELECT 1 FROM Productos_noPreparados 
        WHERE cod_producto_noPreparado = NEW.cod_producto
    );
    
    -- Validar que no quede stock negativo para salidas
    SELECT CASE
        WHEN NEW.tipo_movimiento = 'salida' 
        AND EXISTS (
            SELECT 1 FROM Productos_noPreparados 
            WHERE cod_producto_noPreparado = NEW.cod_producto 
            AND cant_actual < 0
        )
        THEN RAISE(ABORT, 'Stock insuficiente para el producto: ')
    END;
END;
"""

ALL_TRIGGERS = [
    MOVIMIENTO_COMPRA_TRIGGER_BEFORE,
    INGRESAR_NOPREPARADO_TRIGGER,
    VENTA_COMPLETA_TRIGGER,
    MOVIMIENTO_GENERAL_TRIGGER
]

print("Creando Triggers en:", db_path)

def create_triggers():
    conn = None 
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for trigger in ALL_TRIGGERS:
            cursor.execute(trigger)
        conn.commit()
        print("Triggers creado correctamente.")

        
    except sqlite3.Error as e:
        print(f"Ha ocurido un error creando los triggers: {e}")
        if conn:
            conn.rollback() 
    finally:
        if conn:
            conn.close()
            
if __name__ == "__main__":
    create_triggers()


# def create_triggers(conn):
#     cursor = conn.cursor()
#     for trigger in ALL_TRIGGERS:
#         cursor.execute(trigger)
#     conn.commit()