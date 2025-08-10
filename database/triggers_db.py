import sqlite3
from database import db_path

#actualiza el stock de productos, despues del cambio en la tabla de movimientos a causa de una compra
COMPRA_INVENTARIO_TRIGGER_BEFORE = """
CREATE TRIGGER IF NOT EXISTS tr_after_inventario_insert
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

ALL_TRIGGERS = [
    COMPRA_INVENTARIO_TRIGGER_BEFORE,
    INGRESAR_NOPREPARADO_TRIGGER,
    # añadir más triggers aquí
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