import bcrypt

def hash_password(password):
    """Genera un hash seguro para una contraseña."""
    # .encode('utf-8') es crucial para bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password_bytes):
    """Verifica una contraseña contra un hash existente."""
    # El hash de la BD (hashed_password_bytes) ya está en 'bytes'
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password_bytes)
