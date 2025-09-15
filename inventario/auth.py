import requests
from .config import token_valido, token_productos, url_productos

# funcion para armar la autorizacion y llamar a producto
def crear_cabecera_para_llamar_a_productos():
    return {"Authorization": f"Bearer {token_productos}"}

# funcion para validar el token y permitir cargar (o no) productos
def validar_token(header_de_autorizacion):
    return header_de_autorizacion and header_de_autorizacion.startswith("Bearer ") and header_de_autorizacion.split(" ", 1)[1] == token_valido

# funcion para verificar si existe un producto para poder guardar el producto en el stock
def existe_producto(id_producto: int) -> bool:
    try:
        respuesta_http_de_productos = requests.get(f"{url_productos}/productos/{id_producto}", headers=crear_cabecera_para_llamar_a_productos(),  timeout=2)
        # si la respuesta es 200 (exito) o sea existe el producto, retornamos true
        return respuesta_http_de_productos.status_code == 200
    except:
        return False