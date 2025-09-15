import time, requests, logging
from .auth import armar_header_para_inventario

# guardamos el estado del circuito
estado_corta_circuito = {'fallas_seguidas': 0, 'abierto_hasta': 0}

MAXIMAS_FALLAS = 3
TIEMPO_ABIERTO_DE_BLOQUEO = 10

# funcion para hacer post con reintentos y ciruit breaker
def enviar_post_con_reintentos(url, body, intentos=2, espera=0.3): # segundos de pausas entre reintentos
    hora_actual_en_segundos = time.time()
    
    # si el circuito esta abierto, devolvemos error 503 sin intentar
    if estado_corta_circuito['abierto_hasta'] > hora_actual_en_segundos:

        return type('Respuesta_falso', (), {'status_code': 503, 'json': lambda: {'error': 'circuito_abierto'}})()
    
    # intentamos varias veces (1 intento mas reintentos)
    for numero_de_intento in range(intentos + 1):
        try:
            # hacemos la llamada http con timeout de 2 segundos
            respuesta_http = requests.post(url, json=body, headers=armar_header_para_inventario(), timeout=2)
            
            # si el server responde error 5.. lo tratamos como fallo
            if respuesta_http.status_code >= 500:
                raise RuntimeError('inventario_5xx')
            
            # si salio bien, reseteamos las fallas y devolvemos respuesta real
            estado_corta_circuito['fallas_seguidas'] = 0
            logging.info('llamada_inventario_ok')
            return respuesta_http
        
        except Exception as e:
            # cualquier error: sumamos una falla y lo anotamos
            logging.error(f'llamada_inventario_error: {e}')
            estado_corta_circuito['fallas_seguidas'] += 1
            
            # si llegamos al maximo de fallas -> abrimos circuito por 10 seg
            if estado_corta_circuito['fallas_seguidas'] >= MAXIMAS_FALLAS:
                estado_corta_circuito['abierto_hasta'] = time.time() + TIEMPO_ABIERTO_DE_BLOQUEO
                break
            
            # si no llegamos al maximo, esperamos un poco y reintentamos
            time.sleep(espera)
            
    # si fallaron todos los intentos, devolvemos error 503 generico
    return type('Resp', (), {'status_code': 503, 'json': lambda: {'error': 'inventario_no_disponible'}})()