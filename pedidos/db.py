import sqlite3
from .config import ruta_bd

def crear_tabla():
    with sqlite3.connect(ruta_bd) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS pedidos(
            id_pedido INTEGER PRIMARY KEY AUTOINCREMENT, 
            id_producto INTEGER NOT NULL,
            nombre_de_producto TEXT NOT NULL,
            cantidad_solicitada INTEGER NOT NULL)""")
