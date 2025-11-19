from werkzeug.security import generate_password_hash, check_password_hash
import config
import re

def hash_password(password):
    """Genera un hash seguro para una contraseña."""
    return generate_password_hash(password)

def check_password(password, hashed_password):
    """Verifica una contraseña contra un hash existente."""
    # Handle the case where the hash is in the old binary format
    if isinstance(hashed_password, memoryview):
        return False  # Old format is incompatible, so authentication fails
    return check_password_hash(hashed_password, password)

def validate_password(password):
    """
    Valida la complejidad de una contraseña.
    Retorna (is_valid, error_message)
    """
    if not password:
        return False, "La contraseña no puede estar vacía."
    
    if len(password) < config.MIN_PASSWORD_LENGTH:
        return False, f"La contraseña debe tener al menos {config.MIN_PASSWORD_LENGTH} caracteres."
    
    # Validar que tenga al menos un número y una mayúscula (recomendado pero no obligatorio)
    # Solo verificamos longitud mínima como requisito obligatorio
    
    return True, ""

def validate_username(username):
    """
    Valida el formato del nombre de usuario.
    Retorna (is_valid, error_message)
    """
    if not username:
        return False, "El nombre de usuario no puede estar vacío."
    
    username = username.strip()
    
    if len(username) > config.MAX_USERNAME_LENGTH:
        return False, f"El nombre de usuario no puede exceder {config.MAX_USERNAME_LENGTH} caracteres."
    
    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        return False, "El nombre de usuario solo puede contener letras, números, guiones y guiones bajos."
    
    return True, ""

def validate_full_name(full_name):
    """
    Valida el nombre completo del usuario.
    Retorna (is_valid, error_message)
    """
    if not full_name:
        return False, "El nombre completo no puede estar vacío."
    
    full_name = full_name.strip()
    
    if len(full_name) > config.MAX_FULL_NAME_LENGTH:
        return False, f"El nombre completo no puede exceder {config.MAX_FULL_NAME_LENGTH} caracteres."
    
    return True, ""
