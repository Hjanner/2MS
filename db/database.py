import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv('SQLITE_DB')


def get_connection():
    """Función para obtener conexión a la base de datos"""
    try:
        # Conectar a SQLite (crea el archivo si no existe)
        conn = sqlite3.connect(db_name)        
        cursor = conn.cursor()
        print(f"Conectado a {db_name}")
        print("=" * 60)
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Error de conexión: {e}")
        raise

# Obtener conexión global
conn, cursor = get_connection()