import os
from dotenv import load_dotenv

load_dotenv('.env_pedidos')

token_valido = os.getenv("TOKEN_DE_PEDIDOS")
token_para_productos = os.getenv("TOKEN_DE_PRODUCTOS")
token_para_inventario = os.getenv("TOKEN_DE_INVENTARIO")

url_productos = os.getenv("URL_PRODUCTOS", "http://127.0.0.1:5001")
url_inventario = os.getenv("URL_INVENTARIO", "http://127.0.0.1:5002")

ruta_bd = "base_de_datos_pedidos.sqlite"
