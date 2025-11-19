#!/usr/bin/env python3
"""
Script de Verificación Post-Instalación
Verifica que todos los componentes están correctamente configurados
"""

import sys
import os

def check_python_version():
    """Verifica versión de Python"""
    print("🔍 Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} - Se requiere 3.9+")
        return False

def check_dependencies():
    """Verifica que todas las dependencias están instaladas"""
    print("\n🔍 Verificando dependencias...")
    required = [
        'streamlit',
        'pandas',
        'psycopg2',
        'werkzeug',
        'streamlit_drawable_canvas',
        'streamlit_folium',
        'folium'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NO ENCONTRADO")
            missing.append(package)
    
    return len(missing) == 0

def check_secrets_config():
    """Verifica que secrets.toml está configurado"""
    print("\n🔍 Verificando configuración de secretos...")
    
    secrets_path = ".streamlit/secrets.toml"
    
    if not os.path.exists(secrets_path):
        print(f"   ❌ {secrets_path} no encontrado")
        print(f"      Crea el archivo con:")
        print(f"      mkdir -p .streamlit")
        print(f"      echo 'DB_URL = \"tu_connection_string\"' > {secrets_path}")
        return False
    
    try:
        with open(secrets_path, 'r') as f:
            content = f.read()
            if 'DB_URL' in content and 'postgresql://' in content:
                print(f"   ✅ {secrets_path} configurado")
                return True
            else:
                print(f"   ⚠️  {secrets_path} existe pero no contiene DB_URL válido")
                return False
    except Exception as e:
        print(f"   ❌ Error leyendo {secrets_path}: {e}")
        return False

def check_database_connection():
    """Verifica conexión a la base de datos"""
    print("\n🔍 Verificando conexión a base de datos...")
    
    try:
        import database
        conn = database.get_db_connection()
        
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"   ✅ Conectado a PostgreSQL")
            print(f"      {version[0][:50]}...")
        
        return True
    except Exception as e:
        print(f"   ❌ Error de conexión: {str(e)[:100]}")
        print(f"      Verifica que:")
        print(f"      1. DB_URL es válido en .streamlit/secrets.toml")
        print(f"      2. Tu IP está en el IP Allow List (si usas Neon)")
        print(f"      3. PostgreSQL está corriendo")
        return False

def check_tables():
    """Verifica que las tablas están creadas"""
    print("\n🔍 Verificando tablas de base de datos...")
    
    try:
        import database
        
        tables = [
            'form_areas',
            'usuarios',
            'form_templates',
            'form_submissions'
        ]
        
        conn = database.get_db_connection()
        with conn.cursor() as cur:
            for table in tables:
                cur.execute(f"""
                    SELECT EXISTS(
                        SELECT FROM information_schema.tables 
                        WHERE table_name = '{table}'
                    );
                """)
                exists = cur.fetchone()[0]
                status = "✅" if exists else "❌"
                print(f"   {status} {table}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error verificando tablas: {e}")
        return False

def check_files():
    """Verifica que los archivos principales existen"""
    print("\n🔍 Verificando archivos principales...")
    
    required_files = [
        'app.py',
        'config.py',
        'auth.py',
        'database.py',
        'db_helpers.py',
        'admin_view.py',
        'operator_view.py',
        'init_db.py',
        'datos_centros.csv',
        'requirements.txt'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NO ENCONTRADO")
            missing.append(file)
    
    return len(missing) == 0

def check_csv_data():
    """Verifica que datos_centros.csv está presente y válido"""
    print("\n🔍 Verificando datos de centros...")
    
    if not os.path.exists('datos_centros.csv'):
        print(f"   ❌ datos_centros.csv no encontrado")
        return False
    
    try:
        import pandas as pd
        df = pd.read_csv('datos_centros.csv', encoding='utf-8')
        print(f"   ✅ datos_centros.csv: {len(df)} registros")
        return True
    except Exception as e:
        print(f"   ⚠️  Error leyendo CSV: {e}")
        return False

def check_venv():
    """Verifica que está en un entorno virtual"""
    print("\n🔍 Verificando entorno virtual...")
    
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print(f"   ✅ Entorno virtual activo: {sys.prefix}")
        return True
    else:
        print(f"   ⚠️  No detectado entorno virtual activo")
        print(f"      Activa con: source .venv/bin/activate")
        return False

def main():
    """Ejecuta todas las verificaciones"""
    print("=" * 60)
    print("🔧 VERIFICACIÓN POST-INSTALACIÓN")
    print("=" * 60)
    
    checks = [
        ("Python", check_python_version),
        ("Venv", check_venv),
        ("Dependencias", check_dependencies),
        ("Archivos", check_files),
        ("Secretos", check_secrets_config),
        ("BD Conexión", check_database_connection),
        ("BD Tablas", check_tables),
        ("CSV Datos", check_csv_data),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n⚠️  Error en verificación {name}: {e}")
            results.append((name, False))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nResultado: {passed}/{total} verificaciones pasadas")
    
    if passed == total:
        print("\n🎉 ¡INSTALACIÓN EXITOSA!")
        print("\nPróximos pasos:")
        print("1. Ejecuta: streamlit run app.py")
        print("2. Abre: http://localhost:8501")
        print("3. Login: usuario 'admin', contraseña 'Admin1234'")
        print("4. Cambia la contraseña en la primera sesión")
        return 0
    else:
        print("\n⚠️  Hay problemas que resolver")
        print("Ver arriba las verificaciones fallidas (❌)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
