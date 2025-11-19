#!/bin/bash

# Gestor de Centros Educativos - Setup Script
# Script automatizado para instalar y configurar la aplicación

set -e  # Salir si algo falla

echo "=================================================="
echo "🚀 SETUP GESTOR DE CENTROS EDUCATIVOS"
echo "=================================================="
echo ""

# Verificar Python
echo "✓ Verificando Python..."
python3 --version || { echo "❌ Python 3 no encontrado"; exit 1; }

# Crear entorno virtual
echo "✓ Creando entorno virtual..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "  Entorno virtual creado"
else
    echo "  Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "✓ Activando entorno virtual..."
source .venv/bin/activate

# Actualizar pip
echo "✓ Actualizando pip..."
pip install --upgrade pip > /dev/null 2>&1

# Instalar dependencias
echo "✓ Instalando dependencias..."
pip install -r requirements.txt > /dev/null 2>&1

# Crear directorio .streamlit si no existe
echo "✓ Configurando directorio de secretos..."
mkdir -p .streamlit

# Verificar si secrets.toml existe
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo ""
    echo "=================================================="
    echo "⚠️  CONFIGURACIÓN DE BASE DE DATOS REQUERIDA"
    echo "=================================================="
    echo ""
    echo "Se necesita configurar la conexión a PostgreSQL."
    echo ""
    echo "OPCIÓN 1: Usar Neon (recomendado para desarrollo)"
    echo "  1. Ve a https://neon.tech y crea una cuenta"
    echo "  2. Crea un nuevo proyecto"
    echo "  3. Copia el 'Connection string'"
    echo "  4. ¡IMPORTANTE! Añade tu IP a 'IP Allow List' en Neon"
    echo ""
    echo "OPCIÓN 2: Usar PostgreSQL Local"
    echo "  1. Asegúrate de tener PostgreSQL instalado"
    echo "  2. Crea una base de datos: createdb gestor_centros"
    echo "  3. Connection string: postgresql://usuario:pass@localhost:5432/gestor_centros"
    echo ""
    read -p "Ingresa tu DB_URL: " db_url
    
    if [ -z "$db_url" ]; then
        echo "❌ DB_URL no puede estar vacío"
        exit 1
    fi
    
    cat > .streamlit/secrets.toml << EOF
DB_URL = "$db_url"
EOF
    
    echo "✓ secrets.toml creado"
else
    echo "  secrets.toml ya existe"
fi

# Inicializar base de datos
echo ""
echo "✓ Inicializando base de datos..."
python init_db.py

echo ""
echo "=================================================="
echo "✅ SETUP COMPLETADO CON ÉXITO"
echo "=================================================="
echo ""
echo "Próximos pasos:"
echo ""
echo "1. Activa el entorno virtual (si no está activo):"
echo "   source .venv/bin/activate"
echo ""
echo "2. Inicia la aplicación:"
echo "   streamlit run app.py"
echo ""
echo "3. Abre en tu navegador:"
echo "   http://localhost:8501"
echo ""
echo "4. Credenciales por defecto:"
echo "   Usuario: admin"
echo "   Contraseña: Admin1234"
echo ""
echo "⚠️  IMPORTANTE: Cambia la contraseña en la primera sesión"
echo ""
