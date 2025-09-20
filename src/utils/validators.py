# src/utils/validators.py
# Este módulo proporciona funciones de validación de propósito general
# que pueden ser reutilizadas en diferentes partes de la aplicación.

def validar_no_vacio(texto: str) -> bool:
    """
    Verifica que una cadena de texto no esté vacía ni contenga solo espacios en blanco.
    
    Args:
        texto (str): La cadena a validar.
        
    Returns:
        bool: True si la cadena es válida, False en caso contrario.
    """
    # `bool(texto)` comprueba si la cadena no es None o vacía.
    # `texto.strip()` elimina espacios al inicio y al final, y si el resultado
    # es una cadena vacía, también se evalúa como False.
    return bool(texto and texto.strip())


def validar_numero(texto: str) -> bool:
    """
    Verifica si una cadena de texto puede ser convertida a un número (flotante).
    
    Args:
        texto (str): La cadena a validar.
        
    Returns:
        bool: True si la cadena representa un número, False en caso contrario.
    """
    try:
        # Intenta convertir la cadena a un número de punto flotante.
        float(texto)
        # Si la conversión tiene éxito, la cadena es un número válido.
        return True
    except ValueError:
        # Si la conversión falla (lanza ValueError), la cadena no es un número.
        return False