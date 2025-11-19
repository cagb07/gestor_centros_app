"""
Configuración centralizada del proyecto
"""

# Validaciones de usuario
MIN_PASSWORD_LENGTH = 8
MAX_USERNAME_LENGTH = 50
MAX_FULL_NAME_LENGTH = 100

# Validaciones de formularios
MAX_AREA_NAME_LENGTH = 100
MAX_TEMPLATE_NAME_LENGTH = 100
MAX_FIELD_LABEL_LENGTH = 100

# Roles permitidos
ALLOWED_ROLES = ("admin", "operador")

# Tipos de campos disponibles
FIELD_TYPES = [
    "Texto",
    "Área de Texto",
    "Fecha",
    "Tabla Dinámica",
    "Geolocalización",
    "Firma",
    "Carga de Imagen"
]

# Codificación por defecto para CSV
CSV_ENCODING = 'cp1252'

# Mapeo de columnas CSV a etiquetas de formulario
CSV_TO_FORM_MAP = {
    "CENTRO_EDUCATIVO": "Nombre del Centro",
    "PROVINCIA": "Provincia",
    "CANTON": "Cantón",
    "DISTRITO": "Distrito",
    "DIRECCION": "Dirección",
    "CODSABER": "Código Saber"
}

# Coordenadas por defecto (Centro de Costa Rica)
DEFAULT_MAP_CENTER = [9.9333, -84.0833]
DEFAULT_MAP_ZOOM = 7
