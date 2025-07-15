import sqlite3
import os

# Nombre del archivo de la base de datos
db_name = os.getenv('SQLITE_DB', '2MS.db')

def insert_data():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insertar datos en Clientes
    cursor.execute("INSERT OR IGNORE INTO Clientes (ci_cliente, nombre, tlf, depto_escuela) VALUES (?, ?, ?, ?)",
                   ('V12345678', 'Juan Pérez', '04141234567', 'Ingeniería'))
    cursor.execute("INSERT OR IGNORE INTO Clientes (ci_cliente, nombre, tlf, depto_escuela) VALUES (?, ?, ?, ?)",
                   ('V87654321', 'Ana Gómez', '04149876543', 'Administración'))

    # Insertar datos en Proveedores
    cursor.execute("INSERT OR IGNORE INTO Proveedores (Rif, razon_social, dirección, tfl, persona_contacto) VALUES (?, ?, ?, ?, ?)",
                   ('J123456789', 'Proveedor Uno', 'Calle 1', '02121234567', 'Carlos López'))
    cursor.execute("INSERT OR IGNORE INTO Proveedores (Rif, razon_social, dirección, tfl, persona_contacto) VALUES (?, ?, ?, ?, ?)",
                   ('J987654321', 'Proveedor Dos', 'Calle 2', '02129876543', 'María Ruiz'))

    # Insertar datos en categoria_productos
    cursor.execute("INSERT OR IGNORE INTO categoria_productos (descr, tipo) VALUES (?, ?)",
                   ('Bebidas', 'noPreparado'))
    cursor.execute("INSERT OR IGNORE INTO categoria_productos (descr, tipo) VALUES (?, ?)",
                   ('Comidas', 'preparado'))

    # Insertar datos en Productos
    cursor.execute("INSERT OR IGNORE INTO Productos (cod_producto, nombre, precio, id_categoria, Rif) VALUES (?, ?, ?, ?, ?)",
                   ('P001', 'Coca Cola', 1.5, 1, 'J123456789'))
    cursor.execute("INSERT OR IGNORE INTO Productos (cod_producto, nombre, precio, id_categoria, Rif) VALUES (?, ?, ?, ?, ?)",
                   ('P002', 'Empanada', 2.0, 2, 'J987654321'))

    # Insertar datos en TasasCambio
    cursor.execute("INSERT OR IGNORE INTO TasasCambio (fecha, valor_usd_bs, origen) VALUES (?, ?, ?)",
                   ('2024-06-01', 40.5, 'BCV'))
    cursor.execute("INSERT OR IGNORE INTO TasasCambio (fecha, valor_usd_bs, origen) VALUES (?, ?, ?)",
                   ('2024-06-02', 41.0, 'Manual'))

    # Insertar datos en Ventas
    cursor.execute("INSERT OR IGNORE INTO Ventas (monto_total_bs, iva, fecha, monto_total_usd, tipo, ci_cliente, id_tasa) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (100.0, 16.0, '2024-06-01', 2.5, 'de_contado', 'V12345678', 1))

    # Insertar datos en Compras
    cursor.execute("INSERT OR IGNORE INTO Compras (fecha, Rif) VALUES (?, ?)",
                   ('2024-06-01', 'J123456789'))

    conn.commit()
    conn.close()
    print("Datos de prueba insertados correctamente.")

if __name__ == "__main__":
    insert_data()