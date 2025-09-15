import sqlite3
from .config import ruta_bd

# funcion para crear la base de datos de inventario
def crear_tabla():
    with sqlite3.connect(ruta_bd) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS stock (
            id_producto INTEGER PRIMARY KEY, cantidad_disponible INTEGER NOT NULL)""")
