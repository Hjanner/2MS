import sqlite3
from database import db_path

COMPRA_INVENTARIO_TRIGGER_BEFORE = """
CREATE TRIGGER IF NOT EXISTS tr_after_inventario_insert
AFTER INSERT ON Inventarios
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

ALL_TRIGGERS = [
    COMPRA_INVENTARIO_TRIGGER_BEFORE
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