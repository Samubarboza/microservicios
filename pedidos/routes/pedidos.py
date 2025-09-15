from flask import request
import sqlite3, requests, logging

from ..app import app
from ..config import ruta_bd, url_productos, url_inventario
from ..auth import validar_token, armar_header_para_productos
from ..circuit_breaker import enviar_post_con_reintentos

# endpoint de salud para ver si el servicio funciona
@app.get('/check')
def check():
    return {'estado':'ok'}, 200 # (ok, exito)

# create - crea un pedido nuevo, valida datos, descuenta stock y guarda en la base.
@app.post('/pedidos')
def crear_pedido():
    # 1) seguridad: validar token del cliente
    if not validar_token(request.headers.get('Authorization')):
        return {'error':'no autorizado'}, 401 # no autorizado
    
    # 2, leer y validar datos del pedido
    datos_pedido_json = request.get_json() or {}
    id_producto = int(datos_pedido_json.get('id_producto', 0))
    cantidad_solicitada = int(datos_pedido_json.get('cantidad_solicitada', 0))
    if id_producto <= 0 or cantidad_solicitada <= 0:
        return {'error':'datos invalidos'}, 400 # peticion incorrecta
    
    # registro, llego pedido
    logging.info('pedido_recibido')
    
    # 3, verificar que el producto exista (llamamos a mi microservi de productos), si no responde 200, devolvemos error
    respuesta_producto = requests.get(f'{url_productos}/productos/{id_producto}', headers=armar_header_para_productos(), timeout=2)
    
    if respuesta_producto.status_code != 200:
        logging.warning('producto_no_existe')
        return {'error':'producto no existe'}, 400 # pet, incorecta
    
    # datos del producto
    producto = respuesta_producto.json()
    
    # 4, descontar stock en inventario (salida de stock) con reintentos/circuit/breaker
    respuesta_descuento_inventario = enviar_post_con_reintentos(f'{url_inventario}/stock/salir', {'id_producto': id_producto, 'cantidad_a_salir': cantidad_solicitada})
    
    # 4a, si no hay stock suficiente, devolvemos 409
    if respuesta_descuento_inventario.status_code == 409:
        logging.warning('sin_stock_suficiente')
        return {'error':'sin stock suficiente'}, 409 # conflicto, 
    
    # 4b, si inventario fallo (timeouts/5xx/circuito abierto), devolver 502
    if respuesta_descuento_inventario.status_code != 200:
        logging.error('fallo_inventario_o_circuito')
        return {'error':'fallo inventario'}, 502 # bad gateway - error con el serviio 
    
    # 5, guardamos el pedido en la base local de la tabla de pedidos
    with sqlite3.connect(ruta_bd) as db:
        db.execute('INSERT INTO pedidos (id_producto, nombre_de_producto, cantidad_solicitada) VALUES(?,?,?)', (id_producto, producto['nombre_de_producto'], cantidad_solicitada))
        
        # devuelve el id autogenerado de la ultima fila insertada en esta conexion
        id_producto_creado = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        
    # registro, pedido confirmado
    logging.info('pedido_confirmado')
    
    # 6, responder al cliente con el pedido creado
    return {'id_pedido': id_producto_creado, 'id_producto':id_producto, 'nombre_del_producto': producto['nombre_de_producto'], 'cantidad_solicitada':cantidad_solicitada}, 201 # creado correctamente
        
        