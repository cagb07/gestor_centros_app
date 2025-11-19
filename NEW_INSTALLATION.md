# 📦 Gestión de Instalación Nueva - Checklist Completo

## 🎯 Objetivo
Guiar a un nuevo usuario a través de la instalación y verificación de la aplicación Gestor de Centros Educativos.

---

## 📋 FASE 1: Requisitos Previos (5 min)

### ✅ Verificar Requisitos Mínimos

```bash
# 1. Python 3.9+
python3 --version
# Esperado: Python 3.9.x o superior

# 2. Git
git --version
# Esperado: git version...

# 3. PostgreSQL (local) O Neon (cuenta)
# - Local: sudo service postgresql status
# - Neon: https://neon.tech
```

### ✅ Preparar Ambiente

- [ ] Decidir dónde instalar (carpeta del proyecto)
- [ ] Crear carpeta de trabajo
- [ ] Abrir terminal/CMD en esa carpeta
- [ ] Tener a mano credenciales de BD (PostgreSQL local o Neon)

---

## 📋 FASE 2: Setup Rápido (10 min)

### Opción A: Setup Automático (Recomendado)

```bash
# 1. Clonar
git clone https://github.com/cagb07/gestor_centros_app.git
cd gestor_centros_app

# 2. Ejecutar setup
chmod +x setup.sh     # Linux/Mac
./setup.sh            # Linux/Mac

# O para Windows, ejecutar manualmente (ver Opción B)
```

**Qué hace setup.sh:**
- ✅ Crea entorno virtual
- ✅ Instala dependencias
- ✅ Pide connection string
- ✅ Crea .streamlit/secrets.toml
- ✅ Ejecuta init_db.py
- ✅ Muestra resumen

---

### Opción B: Setup Manual (Linux/Mac/Windows)

```bash
# 1. Clonar
git clone https://github.com/cagb07/gestor_centros_app.git
cd gestor_centros_app

# 2. Crear venv
python3 -m venv .venv

# 3. Activar venv
source .venv/bin/activate        # Linux/Mac
# O
.venv\Scripts\activate           # Windows

# 4. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 5. Crear secrets.toml
mkdir -p .streamlit
# Edita con tu editor favorito o:
cat > .streamlit/secrets.toml << EOF
DB_URL = "TU_CONNECTION_STRING_AQUI"
EOF

# 6. Inicializar BD
python init_db.py

# 7. Verificar instalación
python verify_installation.py
```

---

## 📋 FASE 3: Configurar Base de Datos (5-15 min)

### Opción I: Usar Neon (Más fácil)

**Pasos:**
1. Ve a https://neon.tech
2. Registrate con GitHub o Email
3. Crea un nuevo proyecto
4. Espera 2-3 min a que se cree
5. Ve a "Connection String" y copia el string completo
6. **IMPORTANTE:** Settings → IP Allow List → Add tu IP (de https://ifconfig.me)
7. Usa el string en `.streamlit/secrets.toml`

**Formato esperado:**
```toml
DB_URL = "postgresql://usuario:xxxxx@xxxxx.neon.tech:5432/databasename?sslmode=require"
```

---

### Opción II: Usar PostgreSQL Local

**Pasos:**
1. Instala PostgreSQL desde https://www.postgresql.org/download
2. Abre psql (terminal de PostgreSQL)
3. Crea BD:
   ```sql
   CREATE DATABASE gestor_centros;
   ```
4. Crea string de conexión:
   ```toml
   DB_URL = "postgresql://postgres:tu_contraseña@localhost:5432/gestor_centros"
   ```
5. Usa este string en `.streamlit/secrets.toml`

---

## 📋 FASE 4: Inicialización de BD (2 min)

```bash
python init_db.py
```

**Salida esperada:**
```
--- INICIALIZADOR DE BASE DE DATOS ---
Conectando a la base de datos...
✅ ¡Conexión exitosa y tablas creadas!
Creando usuario 'admin'...
✅ Usuario admin 'admin' creado.

✅ ¡Inicialización completada con éxito!
Usuario: admin
Pass: Admin1234

Ahora ejecuta: streamlit run app.py
```

---

## 📋 FASE 5: Verificación (3 min)

```bash
python verify_installation.py
```

**Salida esperada:**
```
🔧 VERIFICACIÓN POST-INSTALACIÓN
============================================================

🔍 Verificando versión de Python...
   ✅ Python 3.11.5 - OK

🔍 Verificando entorno virtual...
   ✅ Entorno virtual activo: /path/to/.venv

🔍 Verificando dependencias...
   ✅ streamlit
   ✅ pandas
   ... (más dependencias)

...

📊 RESUMEN
============================================================
✅ Python
✅ Venv
✅ Dependencias
✅ Archivos
✅ Secretos
✅ BD Conexión
✅ BD Tablas
✅ CSV Datos

Resultado: 8/8 verificaciones pasadas

🎉 ¡INSTALACIÓN EXITOSA!
```

---

## 📋 FASE 6: Primera Ejecución (2 min)

```bash
streamlit run app.py
```

**Salida esperada:**
```
  Welcome to Streamlit! 🎈

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  Ready to accept connections...
```

---

## 📋 FASE 7: Login y Primeros Pasos (5 min)

1. **Abre en navegador:**
   ```
   http://localhost:8501
   ```

2. **Login como Admin:**
   - Usuario: `admin`
   - Contraseña: `Admin1234`

3. **Cambiar contraseña (IMPORTANTE):**
   - Panel Admin → Gestión de Usuarios
   - Crear nuevo usuario admin con contraseña fuerte
   - Eliminar usuario 'admin' por defecto

4. **Probar funcionalidades:**
   - [ ] Crear área
   - [ ] Crear plantilla con campos
   - [ ] Crear usuario operador
   - [ ] Logout y login como operador
   - [ ] Llenar formulario
   - [ ] Volver a admin y revisar envío

---

## 🐛 Troubleshooting Rápido

| Error | Causa | Solución |
|-------|-------|----------|
| "No se encontró DB_URL" | secrets.toml falta o vacío | Crear `.streamlit/secrets.toml` con DB_URL |
| "Connection refused" | BD no está corriendo o IP bloqueada | Verificar PostgreSQL/Neon, añadir IP a allow list |
| "Módulo no encontrado" | Venv no activo | `source .venv/bin/activate` |
| "Tabla ya existe" | NORMAL en 2ª ejecución | No es error, simplemente verifica tablas existentes |
| "Port 8501 already in use" | Otra instancia de Streamlit corriendo | `lsof -i :8501` y kill, o cambiar port |

---

## 📁 Archivos Importantes (Referencia)

| Archivo | Propósito |
|---------|----------|
| `INSTALL.md` | Guía detallada de instalación |
| `FUNCIONALIDADES.md` | Lista de características |
| `CAMBIOS_IMPLEMENTADOS.md` | Cambios recientes |
| `PRODUCTION.md` | Despliegue en producción |
| `setup.sh` | Script automatizado (Linux/Mac) |
| `verify_installation.py` | Script de verificación |
| `.streamlit/secrets.toml` | Configuración DB (⚠️ NO en git) |
| `requirements.txt` | Dependencias Python |

---

## ✅ Checklist Final

- [ ] Python 3.9+ instalado
- [ ] Git instalado
- [ ] PostgreSQL o Neon configurado
- [ ] Repositorio clonado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] `.streamlit/secrets.toml` creado con DB_URL
- [ ] `init_db.py` ejecutado exitosamente
- [ ] `verify_installation.py` muestra ✅ en todo
- [ ] `streamlit run app.py` funciona
- [ ] Login como admin exitoso
- [ ] Cambió contraseña del admin por defecto
- [ ] Probó crear área/plantilla/usuario
- [ ] Probó como operador llenar formulario
- [ ] Probó marcar envío como revisado

---

## 🎉 ¡Listo!

Si completaste todos los pasos:

✅ La aplicación está funcionando
✅ Puedes crear y gestionar áreas
✅ Puedes crear plantillas de formularios
✅ Puedes gestionar usuarios
✅ Operadores pueden llenar formularios
✅ Puedes revisar envíos como admin

### Próximos Pasos (Opcionales)

1. **Customizar:** Editar colores, logos, textos en `config.py`
2. **Importar datos:** Editar `datos_centros.csv` con tus centros
3. **Desplegar:** Ver `PRODUCTION.md` para Heroku, Docker, etc.
4. **Monitorear:** Configurar logs y backups

---

**¿Necesitas ayuda?**
- Lee `INSTALL.md` para más detalles
- Revisa `PRODUCTION.md` si quieres desplegar
- Consulta `TROUBLESHOOTING.md` si hay errores

**Fecha:** 19 de Noviembre, 2025
