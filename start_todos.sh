# script, lista de instrucciones para la compu
# si alguna instruccion del script falla, para todo
set -e 

# entramos a producot y encendemos el servidor
( cd productos  && PYTHONPATH=.. python3 -m productos.run_productos ) &

# inventario y encendemos el servidor
( cd inventario && PYTHONPATH=.. python3 -m inventario.run_inventario ) &

# pedidos y encendemos el servidor
( cd pedidos    && PYTHONPATH=.. python3 -m pedidos.run_pedidos ) &

echo "Servicios levantados: productos:5001, inventario:5002, pedidos:5003"
echo "Para detener: pkill -f run_productos.py; pkill -f run_inventario.py; pkill -f run_pedidos.py"
wait

# correr el script con este comando chmod +x start_todos.sh - - ./start_todos.sh


# para matar el script, ( por las dudas )
# lsof -ti:5001 -ti:5002 -ti:5003 | xargs kill -9
