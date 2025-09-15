import sqlite3
from .config import ruta_bd

def crear_tabla():
    with sqlite3.connect(ruta_bd) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS productos(
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_de_producto TEXT NOT NULL,
            precio_del_producto REAL NOT NULL)""")
