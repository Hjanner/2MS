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

ALL_VIEWS = [
    PRODUCTOS_COMPLETOS_VIEW
    # añadir más triggers aquí
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