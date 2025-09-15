import os
from dotenv import load_dotenv

# leemos las variables de entorno
load_dotenv('.env_inventario')

# buscamos en el entorno las variables
token_valido = os.getenv("TOKEN_DE_INVENTARIO")
token_productos = os.getenv("TOKEN_DE_PRODUCTOS")

# nombre del archivo de bd
ruta_bd = "base_de_datos_inventario.sqlite"

# url base del servicio productos - inventario no sabe que productos existen
url_productos = os.getenv("URL_PRODUCTOS", "http://127.0.0.1:5001")
