from pedidos.db import crear_tabla
from pedidos import app

if __name__ == "__main__":
    crear_tabla()
    app.run(port=5003, debug=True)
