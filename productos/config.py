import os
from dotenv import load_dotenv

load_dotenv('.env_productos')

token_valido = os.getenv("TOKEN_DE_PRODUCTOS")
ruta_bd = "base_de_datos_productos.sqlite"
