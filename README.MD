# Microservicios — Penguin Academy (CodePro)

Sistema simple dividido en **3 microservicios** para una tienda: **productos**, **inventario** y **pedidos**.  
Cada servicio tiene **responsabilidad única**, **API REST**, **token** propio y **base de datos independiente** (SQLite).

> Carpetas: `productos/`, `inventario/`, `pedidos/` y script `start_todos.sh`.  
> (Se ven en el repo público).  

## Arquitectura (resumen)

- **Servicio de Productos**
  - CRUD de productos: nombre, precio.
  - Endpoints típicos:  
    - `GET /productos/:id` — ver un producto  
    - `POST /productos` — crear  
    - `PUT /productos/:id` — actualizar  
    - `DELETE /productos/:id` — eliminar  
    - `GET /check` — healthcheck
- **Servicio de Inventario**
  - Stock por producto.  
  - Endpoints típicos:  
    - `GET /stock/:id_producto` — ver stock  
    - `POST /stock/descontar` — descontar stock  
    - `POST /stock/agregar` — reponer stock  
    - `GET /check` — healthcheck
- **Servicio de Pedidos**
  - Crea pedidos y **coordina** con Productos/Inventario.  
  - Endpoints típicos:  
    - `POST /pedidos` — crear pedido (`{ id_producto, cantidad }`)  
    - `GET /pedidos/:id` — ver pedido  
    - `GET /check` — healthcheck

> Comunicación entre servicios: HTTP con `Authorization: Bearer <token_del_servicio>`.

## Reglas y seguridad

- **Cada microservicio**:
  - Su **propia base** (SQLite).  
  - **Token** propio para validar llamadas entrantes.  
  - **Respuestas JSON** y **códigos HTTP** claros:
    - `200 OK`, `201 Created`
    - `400 Datos inválidos`, `401 No autorizado`, `404 No encontrado`
    - `409 Conflicto (sin stock)`, `502 Falla de servicio dependiente`
- Diseño para fallar: logs, timeouts y manejo de errores (circuit breaker simple a nivel de respuestas y reintentos).

## Requisitos previos

- **Python 3.10+**
- Crear y activar un **virtualenv** (opcional recomendado).
- Instalar dependencias en cada servicio (`pip install -r requirements.txt`) si están definidas.

## Variables de entorno (sugeridas)

Cada servicio puede leer:

- `PUERTO` — puerto HTTP (ej. 5001, 5002, 5003)
- `TOKEN_SERVICIO` — token que valida `Authorization: Bearer ...`
- `RUTA_BD` — ruta al archivo SQLite (por servicio)

> Si hay archivo `.env`, mantenerlo **fuera de git** (agregado en `.gitignore`).

## Cómo ejecutar

### Opción A: por servicio (terminales separadas)

```bash
# Productos
cd productos
export PUERTO=5001 TOKEN_SERVICIO=token_productos RUTA_BD=productos.db
python app.py

# Inventario
cd inventario
export PUERTO=5002 TOKEN_SERVICIO=token_inventario RUTA_BD=inventario.db
python app.py

# Pedidos
cd pedidos
export PUERTO=5003 TOKEN_SERVICIO=token_pedidos RUTA_BD=pedidos.db
python app.py
````

### Opción B: script general

Si tu repo incluye `start_todos.sh`, puedes usarlo para levantar todo más rápido.

```bash
bash start_todos.sh
```

## Ejemplos de uso (cURL)

> Reemplazar `<TOKEN>` por el token del servicio destino.
**Ver producto**

```bash
curl -H "Authorization: Bearer <TOKEN>" http://localhost:5001/productos/1
```

**Crear pedido**

```bash
curl -X POST http://localhost:5003/pedidos \
  -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '{"id_producto":1, "cantidad":3}'
```

**Ver stock**

```bash
curl -H "Authorization: Bearer <TOKEN>" http://localhost:5002/stock/1
```

## Decisiones de diseño

* **Dominio claro** por servicio (Single Responsibility).
* **BD por servicio** para evitar acoplamiento.
* **Tokens independientes** para que ningún servicio tenga más permisos de los necesarios.
* **HTTP + JSON** simple y predecible.
* **Healthchecks `/check`** para verificar estado rápido.

## Licencia

MIT (o la que desees).

```

¿Querés que lo suba con algún ajuste (autor, licencia específica, comandos exactos de tus `app.py`, etc.)?
::contentReference[oaicite:0]{index=0}
```
