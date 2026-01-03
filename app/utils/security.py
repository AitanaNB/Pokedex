"""
Utilidades para manejo de contraseñas con hash seguro usando bcrypt.
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Genera un hash seguro de la contraseña usando bcrypt.
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        str: Hash de la contraseña
    """
    # Generar salt y hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(password: str, hashed: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.
    
    Args:
        password: Contraseña en texto plano
        hashed: Hash almacenado de la contraseña (string desde BD)
        
    Returns:
        bool: True si la contraseña es correcta
    """
    # Si hashed es string, convertir a bytes. Si ya es bytes, usarlo directamente
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')
    
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
