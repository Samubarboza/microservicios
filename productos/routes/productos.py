from flask import request
import sqlite3
from ..app import app
from ..config import ruta_bd
from ..auth import validar_token

@app.get("/check")
def probar_servicio():
    return {"estado":"ok"}, 200

@app.post("/productos")
def crear_producto():
    if not validar_token(request.headers.get("Authorization")):
        return {"error":"no autorizado"}, 401

    json_del_producto_recibido = request.get_json() or {}
    nombre_del_producto = json_del_producto_recibido.get("nombre_de_producto")
    precio_del_producto = float(json_del_producto_recibido.get("precio_del_producto", 0))

    if not nombre_del_producto or precio_del_producto <= 0:
        return {"error":"datos invalidos"}, 400

    with sqlite3.connect(ruta_bd) as db:
        consulta_insert_producto = db.execute(
            "INSERT INTO productos(nombre_de_producto, precio_del_producto) VALUES(?,?)",
            (nombre_del_producto, precio_del_producto)
        )
        id_de_producto_insertado = consulta_insert_producto.lastrowid # devolvemos el id autogenerado de la ultima fila de la bd

    return {"id_producto": id_de_producto_insertado,
            "nombre_de_producto": nombre_del_producto,
            "precio_del_producto": precio_del_producto}, 201

# para consultar producto de la base de datos
@app.get("/productos/<int:id_producto>")
def obtener_producto(id_producto):
    if not validar_token(request.headers.get("Authorization")):
        return {"error":"no autorizado"}, 401

    with sqlite3.connect(ruta_bd) as db:
        producto_encontrado = db.execute(
            "SELECT id_producto, nombre_de_producto, precio_del_producto FROM productos WHERE id_producto=?",
            (id_producto,)
        ).fetchone() # traemos la primera fila encontrada

    return ({"id_producto": producto_encontrado[0],
            "nombre_de_producto": producto_encontrado[1],
            "precio_del_producto": producto_encontrado[2]}
            if producto_encontrado else ({"error":"no encontrado"}, 404))
