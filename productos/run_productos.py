from productos.db import crear_tabla
from productos import app

if __name__ == "__main__":
    crear_tabla()
    app.run(port=5001, debug=True)
