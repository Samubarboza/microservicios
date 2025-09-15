# run_inventario.py
from inventario.db import crear_tabla
from inventario import app

if __name__ == "__main__":
    crear_tabla()
    app.run(port=5002, debug=True)
