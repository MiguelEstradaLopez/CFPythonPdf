# src/utils/validators.py

def validar_no_vacio(texto: str) -> bool:
    return bool(texto and texto.strip())


def validar_numero(texto: str) -> bool:
    try:
        float(texto)
        return True
    except ValueError:
        return False
