from .config import token_valido, token_para_productos, token_para_inventario

def validar_token(header_que_envia_el_cliente):
    return header_que_envia_el_cliente and header_que_envia_el_cliente.startswith("Bearer ") and header_que_envia_el_cliente.split(" ",1)[1]==token_valido

def armar_header_para_productos():
    return {"Authorization": f"Bearer {token_para_productos}"}

def armar_header_para_inventario():
    return {"Authorization": f"Bearer {token_para_inventario}"}
