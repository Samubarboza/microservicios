from flask import request
import sqlite3

from ..app import app
from ..config import ruta_bd
from ..auth import validar_token, existe_producto

@app.get("/check")
def check():
    return {"estado": "ok"}, 200


# read
@app.get("/stock/<int:id_producto>")
def obtener_stock(id_producto):
    # validamos que el token sea correcto
    if not validar_token(request.headers.get("Authorization")):
        return {"error": "no autorizado"}, 401
    with sqlite3.connect(ruta_bd) as db:
        resultado_de_la_consulta_del_stock = db.execute("SELECT cantidad_disponible FROM stock WHERE id_producto=?", (id_producto,)).fetchone()
    # si existe devuelve un json con el id del producto y la cantidad disponible
    return {"id_producto": id_producto, "cantidad_disponible": (resultado_de_la_consulta_del_stock[0] if resultado_de_la_consulta_del_stock else 0)}

# endpoint para cargar stock de producto - escucha peticiones http post en la ruta stock/entrar
# create - update
@app.post("/stock/entrar")
def entrada_stock():
    # validamos el token
    if not validar_token(request.headers.get("Authorization")):
        return {"error": "no autorizado"}, 401

    datos_json_del_producto = request.get_json() or {}
    # si el cliente no manda campo, dejamos en 0
    id_del_producto = int(datos_json_del_producto.get("id_producto", 0))
    cantidad_del_producto = int(datos_json_del_producto.get("cantidad_a_entrar", 0))

    if id_del_producto <= 0 or cantidad_del_producto <= 0:
        return {"error": "datos invalidos"}, 400
    # si el producto no existe (verificamos por su id) retornamos 404
    if not existe_producto(id_del_producto):
        return {"error": "producto no existe"}, 404

    with sqlite3.connect(ruta_bd) as db:
        consulta_de_stock = db.execute(
            "SELECT cantidad_disponible FROM stock WHERE id_producto=?", (id_del_producto,)).fetchone()
        nueva_cantidad_del_producto = (consulta_de_stock[0] if consulta_de_stock else 0) + cantidad_del_producto
        db.execute(
            "INSERT OR REPLACE INTO stock (id_producto, cantidad_disponible) VALUES (?, ?)",
            (id_del_producto, nueva_cantidad_del_producto)
        )
    return {"id_producto": id_del_producto, "cantidad_disponible": nueva_cantidad_del_producto}

# endpoint para darle salida a un producto del inventario
# update
@app.post("/stock/salir")
def salida_stock():
    if not validar_token(request.headers.get("Authorization")):
        return {"error": "no autorizado"}, 401

    datos_del_producto = request.get_json() or {}
    id_del_producto = int(datos_del_producto.get("id_producto", 0))
    cantidad_del_producto_a_restar = int(datos_del_producto.get("cantidad_a_salir", 0))

    if id_del_producto <= 0 or cantidad_del_producto_a_restar <= 0:
        return {"error": "datos invalidos"}, 400
    # verificamos que el producto exista
    if not existe_producto(id_del_producto):
        return {"error": "producto no existe"}, 404

    # consultamos la cantidad del producto en la base de de datos
    with sqlite3.connect(ruta_bd) as db:
        consulta_el_stock_del_producto = db.execute(
            "SELECT cantidad_disponible FROM stock WHERE id_producto=?", (id_del_producto,)
        ).fetchone()
        cantidad_actual = (consulta_el_stock_del_producto[0] if consulta_el_stock_del_producto else 0)
        # si el stock actual es menor que lo que se quiere sacar devolvemos 409
        if cantidad_actual < cantidad_del_producto_a_restar:
            return {"error": "sin stock suficiente"}, 409  # (conflicto, no se pudo completar)

        nueva_cantidad_actualizada = cantidad_actual - cantidad_del_producto_a_restar
        db.execute(
            "UPDATE stock SET cantidad_disponible=? WHERE id_producto=?",
            (nueva_cantidad_actualizada, id_del_producto)
        )
    return {"id_producto": id_del_producto, "cantidad_disponible": nueva_cantidad_actualizada}
