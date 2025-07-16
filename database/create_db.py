import sqlite3
import os
from database import db_name, db_path


print("Nombre de la base de datos:", db_name)
print("Ruta de la base de datos:", db_path)


# Todas las sentencias CREATE TABLE
schema = """
CREATE TABLE IF NOT EXISTS Clientes (
  ci_cliente TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  tlf TEXT,
  depto_escuela TEXT
);

CREATE TABLE IF NOT EXISTS Ventas (
  id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
  monto_total_bs REAL,
  fecha DATE,
  monto_total_usd REAL,
  tipo TEXT CHECK (tipo IN ('credito', 'de_contado')),
  ci_cliente TEXT,
  id_tasa INTEGER,
  FOREIGN KEY (ci_cliente) REFERENCES Clientes(ci_cliente),
  FOREIGN KEY (id_tasa) REFERENCES TasasCambio(id_tasa)
);

CREATE TABLE IF NOT EXISTS TasasCambio (
  id_tasa INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha DATE,
  valor_usd_bs REAL,
  origen TEXT CHECK (origen IN ('BCV', 'Manual'))
);


CREATE TABLE IF NOT EXISTS categoria_productos (
  id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
  descr TEXT,
  tipo TEXT CHECK (tipo IN ('preparado', 'noPreparado'))
);

CREATE TABLE IF NOT EXISTS Productos (
  cod_producto TEXT PRIMARY KEY,
  nombre TEXT,
  precio REAL,
  id_categoria INTEGER,
  FOREIGN KEY (id_categoria) REFERENCES categoria_productos(id_categoria)
);

CREATE TABLE IF NOT EXISTS Proveedores (
  Rif TEXT PRIMARY KEY,
  razon_social TEXT,
  direccion TEXT,
  tfl TEXT,
  persona_contacto TEXT
);

CREATE TABLE IF NOT EXISTS Compras (
  id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha DATE,
  Rif TEXT,
  FOREIGN KEY (Rif) REFERENCES Proveedores(Rif)
);

CREATE TABLE IF NOT EXISTS Productos_preparados (
  cod_producto_preparado TEXT PRIMARY KEY,
  descr TEXT,
  FOREIGN KEY (cod_producto_preparado) REFERENCES Productos(cod_producto)
);

CREATE TABLE IF NOT EXISTS Productos_noPreparados (
  cod_producto_noPreparado TEXT PRIMARY KEY,
  cant_min INTEGER,
  cant_actual INTEGER,
  costo_compra REAL,
  unidad_medida TEXT,
  Rif TEXT,
  FOREIGN KEY (cod_producto_noPreparado) REFERENCES Productos(cod_producto),
  FOREIGN KEY (Rif) REFERENCES Proveedores(Rif)
);

  CREATE TABLE IF NOT EXISTS Creditos (
    id_credito INTEGER PRIMARY KEY AUTOINCREMENT,
    ci_cliente TEXT,
    fecha_credito DATE,
    fecha_ultimo_abono DATE,
    fecha_tope_pago DATE,
    monto_total REAL,
    monto_pagado REAL,
    estado TEXT CHECK (estado IN ('Pagado', 'Pendiente', 'Parcial')),
    FOREIGN KEY (ci_cliente) REFERENCES Clientes(ci_cliente)
  );

CREATE TABLE IF NOT EXISTS Pagos (
  id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
  id_venta INTEGER,
  num_cor TEXT,
  monto REAL,
  fecha_pago DATE,
  metodo_pago TEXT CHECK (metodo_pago IN (
    'efectivo_bs', 'efectvo_usd', 'pago_movil', 'debito', 'transferencia')),
  referencia TEXT,
  num_tefl TEXT,
  FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta)
);

CREATE TABLE IF NOT EXISTS Inventarios (
  id_inventario INTEGER PRIMARY KEY AUTOINCREMENT,
  cod_producto TEXT,
  referencia TEXT CHECK (referencia IN ('compra', 'venta', 'descarte', 'ajuste', 'traslado_tienda', 'autoconsumo')),
  comentario TEXT,
  tipo_movimiento TEXT CHECK (tipo_movimiento IN ('entrada', 'salida')),
  cant_movida INTEGER,
  fc_actualizacion DATE,
  FOREIGN KEY (cod_producto) REFERENCES Productos(cod_producto)
);

CREATE TABLE IF NOT EXISTS Detalle_Venta (
  id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
  id_venta INTEGER,
  id_producto TEXT,
  cantidad_producto INTEGER,
  precio_unitario REAL,
  FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta),
  FOREIGN KEY (id_producto) REFERENCES Productos(cod_producto)
);

CREATE TABLE IF NOT EXISTS Compra_Inventario (
  id_compra INTEGER,
  id_inventario INTEGER,
  cod_producto TEXT,
  cant_comprada INTEGER,
  monto_unitario REAL,
  PRIMARY KEY (id_compra, id_inventario, cod_producto),
  FOREIGN KEY (id_compra) REFERENCES Compras(id_compra),
  FOREIGN KEY (id_inventario) REFERENCES Inventarios(id_inventario),
  FOREIGN KEY (cod_producto) REFERENCES Productos(cod_producto)
);
"""

def create_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print(f"Base de datos y tablas creadas en {db_name}")

if __name__ == "__main__":
    create_database()