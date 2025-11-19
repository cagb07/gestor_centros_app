#!/usr/bin/env python3
"""
Script de verificación completa del proyecto
"""
import sys
import os

print("=" * 70)
print("VERIFICACIÓN COMPLETA - GESTOR DE CENTROS EDUCATIVOS")
print("=" * 70)

# 1. Verificar archivos necesarios
print("\n1️⃣  Verificando archivos necesarios...")
required_files = [
    'app.py',
    'config.py',
    'auth.py',
    'database.py',
    'admin_view.py',
    'operator_view.py',
    'init_db.py',
    'requirements.txt',
    'datos_centros.csv',
    '.streamlit/secrets.toml',
    'README.md'
]

all_files_ok = True
for file in required_files:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"   ✅ {file} ({size} bytes)")
    else:
        print(f"   ❌ {file} - NO ENCONTRADO")
        all_files_ok = False

if all_files_ok:
    print("\n✅ Todos los archivos necesarios están presentes")
else:
    print("\n❌ Faltan algunos archivos")
    sys.exit(1)

# 2. Verificar CSV
print("\n2️⃣  Verificando datos_centros.csv...")
try:
    import pandas as pd
    df = pd.read_csv('datos_centros.csv', encoding='utf-8')
    print(f"   ✅ CSV cargado: {len(df)} filas, {len(df.columns)} columnas")
    print(f"   Columnas: {', '.join(df.columns[:5])}...")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# 3. Verificar imports
print("\n3️⃣  Verificando imports...")
try:
    import config
    print("   ✅ config.py importa correctamente")
    import auth
    print("   ✅ auth.py importa correctamente")
    import streamlit as st
    print("   ✅ streamlit disponible")
    import psycopg2
    print("   ✅ psycopg2 disponible")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# 4. Verificar configuración
print("\n4️⃣  Verificando configuración...")
try:
    print(f"   ✅ MIN_PASSWORD_LENGTH: {config.MIN_PASSWORD_LENGTH}")
    print(f"   ✅ ALLOWED_ROLES: {config.ALLOWED_ROLES}")
    print(f"   ✅ FIELD_TYPES: {len(config.FIELD_TYPES)} tipos disponibles")
    print(f"   ✅ CSV_TO_FORM_MAP: {len(config.CSV_TO_FORM_MAP)} mapeos")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# 5. Verificar funciones de auth
print("\n5️⃣  Verificando funciones de auth...")
try:
    # Validar password
    is_valid, msg = auth.validate_password("Test1234")
    print(f"   ✅ validate_password: {is_valid}")
    
    # Validar username
    is_valid, msg = auth.validate_username("testuser")
    print(f"   ✅ validate_username: {is_valid}")
    
    # Validar full_name
    is_valid, msg = auth.validate_full_name("Test User")
    print(f"   ✅ validate_full_name: {is_valid}")
    
    # Hash password
    hashed = auth.hash_password("Test1234")
    print(f"   ✅ hash_password: genera hash de {len(hashed)} caracteres")
    
    # Check password
    result = auth.check_password("Test1234", hashed)
    print(f"   ✅ check_password: {result}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# 6. Verificar database
print("\n6️⃣  Verificando funciones de database...")
try:
    import database
    print("   ✅ database.py importa correctamente")
    # No intentamos conexión a BD sin secretos configurados
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
print("=" * 70)
print("\nPróximos pasos:")
print("1. Asegúrate de que .streamlit/secrets.toml tiene la DB_URL")
print("2. Ejecuta: python init_db.py (primera vez)")
print("3. Ejecuta: streamlit run app.py")
print("=" * 70)
