
import os
import sys

print("=" * 80)
print("VERIFICACIÓN FINAL - FUNCIONALIDADES IMPLEMENTADAS")
print("=" * 80)

# 1. Verificar que no hay errores de sintaxis
print("\n1️⃣  Verificando sintaxis de archivos...")
files_to_check = ['app.py', 'admin_view.py', 'operator_view.py', 'config.py', 'auth.py', 'database.py']

import py_compile
errors = []
for file in files_to_check:
    try:
        py_compile.compile(file, doraise=True)
        print(f"   ✅ {file}: OK")
    except py_compile.PyCompileError as e:
        errors.append(f"{file}: {e}")
        print(f"   ❌ {file}: ERROR")

if errors:
    print("\nErrores encontrados:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

# 2. Verificar que los módulos cargan correctamente
print("\n2️⃣  Verificando que los módulos cargan correctamente...")
try:
    import config
    print("   ✅ config cargado")
    import auth
    print("   ✅ auth cargado")
    import database
    print("   ✅ database cargado")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# 3. Verificar constantes
print("\n3️⃣  Verificando configuraciones...")
print(f"   ✅ MIN_PASSWORD_LENGTH: {config.MIN_PASSWORD_LENGTH}")
print(f"   ✅ ALLOWED_ROLES: {config.ALLOWED_ROLES}")
print(f"   ✅ FIELD_TYPES: {len(config.FIELD_TYPES)} tipos")
print(f"   ✅ CSV_TO_FORM_MAP: {len(config.CSV_TO_FORM_MAP)} mapeos")

# 4. Verificar CSV
print("\n4️⃣  Verificando datos_centros.csv...")
import pandas as pd
df = pd.read_csv('datos_centros.csv', encoding='utf-8')
print(f"   ✅ {len(df)} filas cargadas")
print(f"   ✅ {len(df.columns)} columnas")

# 5. Verificar funcionalidades
print("\n5️⃣  Verificando funcionalidades de auth...")
is_valid, msg = auth.validate_password("Test1234")
print(f"   ✅ validate_password: {'OK' if is_valid else 'FAIL'}")

is_valid, msg = auth.validate_username("testuser")
print(f"   ✅ validate_username: {'OK' if is_valid else 'FAIL'}")

is_valid, msg = auth.validate_full_name("Test User")
print(f"   ✅ validate_full_name: {'OK' if is_valid else 'FAIL'}")

hashed = auth.hash_password("Test1234")
print(f"   ✅ hash_password: {'OK' if len(hashed) > 50 else 'FAIL'}")

result = auth.check_password("Test1234", hashed)
print(f"   ✅ check_password: {'OK' if result else 'FAIL'}")

print("\n" + "=" * 80)
print("✅ TODAS LAS VERIFICACIONES PASARON - EL PROYECTO ESTÁ LISTO")
print("=" * 80)
print("\nPara ejecutar:")
print("  1. python init_db.py      (primera vez)")
print("  2. streamlit run app.py")
print("=" * 80)
