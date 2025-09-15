from .config import token_valido

def validar_token(header_valor_autorizacion):
    return (header_valor_autorizacion
            and header_valor_autorizacion.startswith("Bearer ")
            and header_valor_autorizacion.split(" ",1)[1]==token_valido)
