# Gestor de Centros Educativos

Una aplicación Streamlit para gestionar centros educativos con roles de administrador y operador. Ofrece una interfaz amigable para gestionar usuarios, áreas, plantillas de formularios y envíos de datos.

## Características

- 🔐 **Autenticación con roles**: Admin y Operador
- 👨‍💼 **Panel de Admin**: Gestión de usuarios, áreas, plantillas de formularios y revisión de envíos
- 📝 **Panel de Operador**: Llenar formularios dinámicos y ver historial de envíos
- 📊 **Dashboard**: Métricas de envíos por área y usuario
- 🗺️ **Geolocalización**: Captura de coordenadas en mapas
- 📸 **Carga de imágenes**: Soporte para archivos multimedia
- 🔏 **Firma digital**: Canvas para capturar firmas
- 💾 **Base de datos PostgreSQL**: Almacenamiento robusto de datos

## Requisitos Previos

- Python 3.9 o superior
- PostgreSQL con acceso remoto (ej: Neon)
- Git

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd gestor_centros_app
```

### 2. Crear y activar entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

Crea el archivo `.streamlit/secrets.toml` en la raíz del proyecto:

```toml
DB_URL = "postgresql://usuario:contraseña@host:puerto/nombre_db?sslmode=require"
```

**Nota**: Para usar Neon, sigue estos pasos:
1. Crea una cuenta en [neon.tech](https://neon.tech)
2. Crea un proyecto nuevo
3. Copia el connection string
4. Asegúrate de agregar tu dirección IP a la "IP Allow List" en Neon

### 5. Inicializar la base de datos

```bash
python init_db.py
```

Esto creará las tablas necesarias y un usuario admin por defecto:
- **Usuario**: `admin`
- **Contraseña**: `Admin1234`

## Ejecución

```bash
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`

## Estructura del Proyecto

```
gestor_centros_app/
├── app.py                  # Punto de entrada principal
├── config.py               # Configuraciones y constantes
├── auth.py                 # Funciones de autenticación
├── database.py             # Funciones de base de datos
├── admin_view.py           # Interfaz del administrador
├── operator_view.py        # Interfaz del operador
├── init_db.py              # Script de inicialización
├── datos_centros.csv       # Datos iniciales de centros
├── requirements.txt        # Dependencias de Python
├── .streamlit/
│   └── secrets.toml        # Configuración de secretos (NO en git)
└── tests/
    └── test_auth.py        # Pruebas unitarias
```

## Validaciones Implementadas

- ✓ Contraseña mínima de 8 caracteres
- ✓ Validación de nombres de usuario con regex
- ✓ Campos requeridos en formularios
- ✓ Limpieza de espacios en blanco en entradas
- ✓ Límites de longitud en campos
- ✓ Validación de integridad de base de datos
- ✓ Manejo específico de excepciones de BD
- ✓ Rollback explícito en transacciones

## Troubleshooting

### Error: "No se encontró DB_URL"
- Verifica que `.streamlit/secrets.toml` existe y tiene la variable `DB_URL`
- Revisa el formato del connection string

### Error: "Operación no permitida" en base de datos
- Asegúrate de que tu IP está en la "IP Allow List" de Neon
- Verifica que la base de datos está activa (no dormida)

### Error: "Módulo no encontrado"
- Asegúrate de estar en el entorno virtual
- Ejecuta: `pip install -r requirements.txt`

## Licencia

Este proyecto está bajo la Licencia MIT.
