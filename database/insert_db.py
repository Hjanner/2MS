import sqlite3
import os
from database import db_path

print("Ruta de la base de datos:", db_path)

def insert_data():
    conn = None 
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

# --- Inserts para la tabla Clientes (asegurando que existan para las FK) ---
        clientes_data = [
            ('12345678', 'Juan Pérez', '04141234567', 'Ingeniería'),
            ('87654321', 'Ana Gómez', '04149876543', 'Administración'),
            ('11223344', 'Carlos Ruiz', '04245556677', 'Contabilidad')
        ]
        cursor.executemany("INSERT OR IGNORE INTO Clientes (ci_cliente, nombre, tlf, depto_escuela) VALUES (?, ?, ?, ?)", clientes_data)

# --- Inserts para la tabla TasasCambio (asegurando que existan para las FK de Ventas) ---
        tasas_cambio_data = [
            ('2024-07-15', 36.50, 'BCV')
        ]
        cursor.executemany("INSERT OR IGNORE INTO TasasCambio (fecha, valor_usd_bs, origen) VALUES (?, ?, ?)", tasas_cambio_data)

# --- Inserts para la tabla Proveedores ---
        proveedores_data = [
            ('J-12345678-9', 'Distribuidora La Granja C.A.', 'Av. Principal, Edif. Granja, Caracas', '0212-1234567', 'Ana Pérez'),
            ('V-98765432-1', 'Suministros del Campo S.A.', 'Calle 5, Centro Empresarial, Valencia', '0241-9876543', 'Luis García'),
            ('G-54321098-7', 'Alimentos Frescos 2000 C.A.', 'Zona Industrial, Galpón 10, Maracay', '0243-5432109', 'María Rodríguez')
        ]
        cursor.executemany("INSERT OR IGNORE INTO Proveedores (Rif, razon_social, direccion, tfl, persona_contacto) VALUES (?, ?, ?, ?, ?)", proveedores_data)

# --- Inserts para la tabla categoria_productos ---
        categorias_data = [
            ('Mani', 'noPreparado'),
            ('Almuerzos', 'preparado'),
            ('Cenas', 'preparado'),
            ('Snacks', 'noPreparado'),
            ('Refrescos', 'noPreparado'),
            ('Postres', 'preparado')
        ]
        cursor.executemany("INSERT OR IGNORE INTO categoria_productos (descr, tipo) VALUES (?, ?)", categorias_data)

# --- Inserts para la tabla Productos ---
        productos_data = [
            ('PROD001', 'Mani dulce', 35.50, 1),
            ('PROD002', 'Pabellón Criollo', 8.75, 2),
            ('PROD003', 'Lasagna Boloñesa', 9.99, 3),
            ('PROD004', 'Galletas Chispas', 2.10, 4),
            ('PROD005', 'Coca-Cola 1.5L', 3.00, 5),
            ('PROD006', 'Torta de Chocolate', 6.50, 6),
            ('PROD007', 'Agua Mineral 600ml', 1.00, 5),
            ('PROD008', 'Arepas Rellenas', 7.20, 2),
            ('PROD009', 'Papas Fritas Grandes', 3.50, 4),
            ('PROD010', 'Dominó Clásico', 25.00, 1)
        ]
        cursor.executemany("INSERT OR IGNORE INTO Productos (cod_producto, nombre, precio_usd, id_categoria) VALUES (?, ?, ?, ?)", productos_data)

# --- Inserts para la tabla Productos_preparados ---
        productos_preparados_data = [
            ('PROD002', 'Plato típico venezolano con carne mechada, arroz, caraotas y tajadas.'),
            ('PROD003', 'Capas de pasta, carne molida y salsa bechamel.'),
            ('PROD006', 'Bizcocho húmedo de chocolate con glaseado cremoso.'),
            ('PROD008', 'Arepas de maíz rellenas con diversos guisos.')
        ]
        cursor.executemany("INSERT OR IGNORE INTO Productos_preparados (cod_producto_preparado, descr) VALUES (?, ?)", productos_preparados_data)

# --- Inserts para la tabla Productos_noPreparados ---
        productos_no_preparados_data = [
            ('PROD001', 5, 12, 20.00, 'unidad', 'J-12345678-9'),
            ('PROD004', 10, 50, 1.20, 'paquete', 'V-98765432-1'),
            ('PROD005', 20, 100, 1.80, 'unidad', 'V-98765432-1'),
            ('PROD007', 15, 80, 0.60, 'unidad', 'J-12345678-9'),
            ('PROD009', 8, 30, 2.00, 'paquete', 'G-54321098-7'),
            ('PROD010', 3, 8, 15.00, 'unidad', 'J-12345678-9')
        ]
        cursor.executemany("INSERT OR IGNORE INTO Productos_noPreparados (cod_producto_noPreparado, cant_min, cant_actual, costo_compra, unidad_medida, Rif) VALUES (?, ?, ?, ?, ?, ?)", productos_no_preparados_data)

# --- Inserts para la tabla Compras ---
        compras_data = [
            ('2024-07-01', 'J-12345678-9', 100),
            ('2024-07-05', 'V-98765432-1', 200),
            ('2024-07-10', 'G-54321098-7', 120),
            ('2024-07-12', 'J-12345678-9', 122)
        ]
        cursor.executemany("INSERT INTO Compras (fecha, Rif) VALUES (?, ?)", compras_data)

# --- Inserts para la tabla Movimientos (movimientos de entrada por compras) ---
        movimientos_data = [
            ('PROD001', 'compra', 'Compra inicial de mani dulce', 'entrada', 10, '2024-07-01'),
            ('PROD004', 'compra', 'Compra de galletas', 'entrada', 40, '2024-07-05'),
            ('PROD005', 'compra', 'Compra de Coca-Cola', 'entrada', 70, '2024-07-05'),
            ('PROD007', 'compra', 'Compra de agua mineral', 'entrada', 50, '2024-07-10'),
            ('PROD009', 'compra', 'Compra de papas fritas', 'entrada', 25, '2024-07-10'),
            ('PROD010', 'compra', 'Compra de Dominó', 'entrada', 5, '2024-07-12')
        ]
        cursor.executemany("INSERT INTO Movimientos (cod_producto, referencia, comentario, tipo_movimiento, cant_movida, fc_actualizacion) VALUES (?, ?, ?, ?, ?, ?)", movimientos_data)

# --- Inserts para la tabla Compra_Inventario ---
        # cursor.execute("SELECT id_compra FROM Compras ORDER BY id_compra ASC")
        # compra_ids = [row[0] for row in cursor.fetchall()]

        # # Fetch IDs for movimientos (assuming they were inserted in order)
        # cursor.execute("SELECT id_movimiento FROM Movimientos ORDER BY id_movimiento ASC")
        # inventario_ids = [row[0] for row in cursor.fetchall()]

        # # --- Inserts para la tabla Ventas (asociadas a Pagos) ---
        # ventas_data = [
        #     (100.00, '2024-07-01', 2.74, 'credito', '12345678', 1), # Venta 1 (Juan Perez)
        #     (150.00, '2024-07-03', 4.11, 'credito', '87654321', 1), # Venta 2 (Ana Gomez)
        #     (75.00, '2024-07-05', 2.05, 'credito', '11223344', 1)  # Venta 3 (Carlos Ruiz)
        # ]
        # cursor.executemany("INSERT INTO Ventas (monto_total_bs, fecha, monto_total_usd, tipo, ci_cliente, id_tasa) VALUES (?, ?, ?, ?, ?, ?)", ventas_data)

# --- Inserts para la tabla Creditos ---
        creditos_data = [
            # Crédito 1: Pagado completamente
            ('12345678', '2024-07-01', '2024-07-10', '2024-08-01', 100.00, 100.00, 'Pagado'),
            # Crédito 2: Pendiente (sin abonos, fecha de pago futura)
            ('87654321', '2024-07-03', None, '2024-08-03', 150.00, 0.00, 'Pendiente'),
            # Crédito 3: Parcial (abonado parcialmente)
            ('11223344', '2024-07-05', '2024-07-12', '2024-08-05', 75.00, 40.00, 'Parcial'),
            # Crédito 4: Otro crédito pendiente, pero ya con fecha de pago pasada (podría ser para un reporte de mora)
            ('12345678', '2024-06-15', '2024-06-20', '2024-07-01', 50.00, 20.00, 'Parcial')
        ]
        cursor.executemany("INSERT INTO Creditos (ci_cliente, fecha_credito, fecha_ultimo_abono, fecha_tope_pago, monto_total, monto_pagado, estado) VALUES (?, ?, ?, ?, ?, ?, ?)", creditos_data)
        
        conn.commit()
        print("Datos de prueba insertados correctamente.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        if conn:
            conn.rollback() 
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    insert_data()