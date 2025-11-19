# GUÍA DE INSTALACIÓN Y SETUP - Gestor de Centros Educativos

## 📋 Índice
1. [Requisitos Previos](#requisitos-previos)
2. [Setup Rápido (Automático)](#setup-rápido-automático)
3. [Setup Manual](#setup-manual)
4. [Configuración de Base de Datos](#configuración-de-base-de-datos)
5. [Verificación de Instalación](#verificación-de-instalación)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 Requisitos Previos

### Mínimos
- **Python 3.9+** (recomendado 3.10 o 3.11)
- **Git**
- **PostgreSQL** (local o remoto como Neon)

### Verificación Rápida
```bash
python3 --version    # Debe mostrar 3.9+
git --version        # Debe mostrar git version
```

---

## 🚀 Setup Rápido (Automático)

**Para Linux/Mac:**

```bash
# 1. Clonar repositorio
git clone https://github.com/cagb07/gestor_centros_app.git
cd gestor_centros_app

# 2. Ejecutar script de setup
chmod +x setup.sh
./setup.sh

# El script te pedirá:
# - Connection string de PostgreSQL
# - Creará entorno virtual
# - Instalará dependencias
# - Inicializará la BD
```

**Para Windows (PowerShell):**

```powershell
# 1. Clonar repositorio
git clone https://github.com/cagb07/gestor_centros_app.git
cd gestor_centros_app

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Crear secrets.toml manualmente (ver sección siguiente)
# mkdir -p .streamlit
# echo 'DB_URL = "postgresql://..."' > .streamlit\secrets.toml

# 5. Inicializar BD
python init_db.py

# 6. Ejecutar app
streamlit run app.py
```

---

## 📝 Setup Manual (Paso a Paso)

### Paso 1: Clonar y Preparar

```bash
git clone https://github.com/cagb07/gestor_centros_app.git
cd gestor_centros_app
```

### Paso 2: Crear Entorno Virtual

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

Verificar que está activo:
```bash
which python  # En Linux/Mac debe mostrar .venv/bin/python
# En Windows: where python (debe mostrar .venv\Scripts\python.exe)
```

### Paso 3: Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Dependencias instaladas:
- `streamlit` - Framework web
- `pandas` - Procesamiento de datos
- `psycopg2-binary` - Driver PostgreSQL
- `Werkzeug` - Hashing de contraseñas
- `streamlit-drawable-canvas` - Canvas para firmas
- `streamlit-folium` - Mapas interactivos

---

## 🗄️ Configuración de Base de Datos

### Opción 1: Neon (Recomendado para Desarrollo)

**Ventajas:**
- Gratuito
- Sin instalación local
- Acceso remoto desde cualquier lugar
- Backups automáticos

**Pasos:**

1. **Crear Cuenta:**
   - Ve a [neon.tech](https://neon.tech)
   - Registrate con GitHub o Email
   - Confirma tu email

2. **Crear Proyecto:**
   - Click en "New Project"
   - Selecciona región (ej: "us-east-1")
   - Click "Create Project"

3. **Obtener Connection String:**
   - Espera a que se cree el proyecto (2-3 min)
   - Ve a "Connection String"
   - Copia el string completo (se ve así):
     ```
     postgresql://usuario:xxxxx@xxxxx.neon.tech/databasename?sslmode=require
     ```

4. **Configurar IP Allow List (IMPORTANTE):**
   - En el dashboard de Neon
   - Click en tu proyecto → "Settings"
   - "IP Allow List"
   - Click "Add IP"
   - Opción A: Añade tu IP pública (de https://ifconfig.me)
   - Opción B: Usa `0.0.0.0/0` (permite desde cualquier lugar - solo para desarrollo)

5. **Crear secrets.toml:**
   ```bash
   mkdir -p .streamlit
   cat > .streamlit/secrets.toml << EOF
   DB_URL = "postgresql://usuario:xxxxx@xxxxx.neon.tech/databasename?sslmode=require"
   EOF
   ```

### Opción 2: PostgreSQL Local

**Pasos:**

1. **Instalar PostgreSQL:**
   - Linux: `sudo apt-get install postgresql postgresql-contrib`
   - Mac: `brew install postgresql` o desde [postgresql.org](https://www.postgresql.org/download)
   - Windows: Descarga desde [postgresql.org/download/windows](https://www.postgresql.org/download/windows)

2. **Iniciar el servidor:**
   - Linux/Mac: `brew services start postgresql`
   - Windows: El servicio se inicia automáticamente

3. **Crear base de datos:**
   ```bash
   psql -U postgres
   CREATE DATABASE gestor_centros;
   \q
   ```

4. **Crear secrets.toml:**
   ```bash
   mkdir -p .streamlit
   cat > .streamlit/secrets.toml << EOF
   DB_URL = "postgresql://postgres:tu_contraseña@localhost:5432/gestor_centros"
   EOF
   ```
   Reemplaza `tu_contraseña` con la contraseña que configuraste en PostgreSQL.

---

## 🔐 Crear secrets.toml

### Estructura del archivo

```toml
# .streamlit/secrets.toml
DB_URL = "postgresql://usuario:contraseña@host:puerto/nombre_db?sslmode=require"
```

### Ejemplos por BD

**Neon:**
```toml
DB_URL = "postgresql://neon_user:neon_password@us-east-1.neon.tech:5432/neon_db?sslmode=require"
```

**PostgreSQL Local:**
```toml
DB_URL = "postgresql://postgres:password123@localhost:5432/gestor_centros"
```

### ⚠️ Seguridad

- **Nunca** commits `.streamlit/secrets.toml` a Git
- Añade a `.gitignore`:
  ```
  .streamlit/secrets.toml
  .env
  ```
- En producción, usa variables de entorno

---

## 🗄️ Inicializar Base de Datos

```bash
python init_db.py
```

**Salida esperada:**
```
--- INICIALIZADOR DE BASE DE DATOS ---
Leyendo secretos desde .streamlit/secrets.toml...
Conectando a la base de datos...
✅ ¡Conexión exitosa y tablas creadas!

Creando/Verificando usuario 'admin'...
✅ Usuario admin 'admin' creado.

✅ ¡Inicialización completada con éxito!
Usuario: admin
Pass: Admin1234

Ahora ejecuta: streamlit run app.py
```

**Qué hace:**
- Crea todas las tablas (áreas, usuarios, plantillas, envíos)
- Añade columnas de auditoría (reviewed, reviewed_by, reviewed_at)
- Crea usuario admin con credenciales por defecto
- Si las tablas ya existen, simplemente las verifica

---

## ▶️ Ejecutar la Aplicación

```bash
# Asegúrate de que el entorno virtual está activo
streamlit run app.py
```

**Salida esperada:**
```
  Welcome to Streamlit!

  ...

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  Ready to accept connections...
```

Abre en tu navegador: `http://localhost:8501`

---

## ✅ Verificación de Instalación

### Checklist Rápido

```bash
# 1. Verificar Python
python3 --version
# Debe mostrar 3.9 o superior

# 2. Verificar entorno virtual
which python  # Debe incluir .venv
# (En Windows: where python)

# 3. Verificar pip (dentro del venv)
pip list
# Debe mostrar: streamlit, pandas, psycopg2-binary, etc.

# 4. Verificar secrets.toml
ls -la .streamlit/secrets.toml
# (En Windows: dir .streamlit\secrets.toml)

# 5. Verificar conexión a BD
python -c "import database; conn = database.get_db_connection(); print('✅ Conexión OK')"

# 6. Verificar tablas en BD
psql $DB_URL -c "\dt"
# Debe mostrar: form_areas, usuarios, form_templates, form_submissions
```

---

## 🐛 Troubleshooting

### Error: "No se encontró DB_URL en secrets.toml"

**Causa:** Archivo `.streamlit/secrets.toml` no existe o está malformado

**Solución:**
```bash
# Verificar que existe
ls .streamlit/secrets.toml

# Si no existe, créalo:
mkdir -p .streamlit
echo 'DB_URL = "tu_connection_string_aqui"' > .streamlit/secrets.toml

# Verificar contenido
cat .streamlit/secrets.toml
```

---

### Error: "Error de conexión a la base de datos" o "Connection refused"

**Causa Posible 1: IP no está en Neon Allow List**

**Solución:**
```bash
# 1. Obtén tu IP pública
curl https://ifconfig.me

# 2. Ve a Neon Dashboard
# 3. Tu Proyecto → Settings → IP Allow List
# 4. Add "tu_ip/32" o "0.0.0.0/0"

# 5. Intenta de nuevo
python init_db.py
```

**Causa Posible 2: Base de datos está dormida**

**Solución (Neon):**
- Va al dashboard de Neon
- Click en tu proyecto → "Wake up"
- O configura el proyecto como siempre activo (plan pago)

**Causa Posible 3: PostgreSQL no está corriendo**

**Solución (Local):**
```bash
# Linux
sudo service postgresql start

# Mac
brew services start postgresql

# Windows: Verifica que el servicio está iniciado en Services.msc
```

---

### Error: "Tabla 'usuarios' ya existe"

**Esto es normal.** El script usa `CREATE TABLE IF NOT EXISTS`.

Simplemente significa que ya fue ejecutado antes. No hay problema.

---

### Error: "psycopg2: no module named 'psycopg2'"

**Solución:**
```bash
# Asegúrate de estar en el entorno virtual
source .venv/bin/activate

# Reinstala psycopg2-binary
pip uninstall psycopg2-binary psycopg2
pip install psycopg2-binary

# O usa la versión compilada
pip install psycopg2
```

---

### Error: "ModuleNotFoundError: No module named 'streamlit'"

**Causa:** Entorno virtual no activo

**Solución:**
```bash
# Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows

# Reinstalar dependencias
pip install -r requirements.txt

# Ejecutar app
streamlit run app.py
```

---

### Error: "Permission denied" en setup.sh

**Solución:**
```bash
chmod +x setup.sh
./setup.sh
```

---

### Error: "yaml.scanner.ScannerError" en Streamlit

**Solución:** Añade espacios en `.streamlit/config.toml`:
```toml
[client]
showErrorDetails = true
```

---

## 🔑 Credenciales Iniciales

Tras ejecutar `init_db.py`:

| Propiedad | Valor |
|-----------|-------|
| **Usuario** | `admin` |
| **Contraseña** | `Admin1234` |
| **Rol** | Admin |

⚠️ **IMPORTANTE:** Cambia estas credenciales en la primera sesión creando un nuevo admin y eliminando este.

---

## 🔄 Verificación Final

1. **Abre la app:**
   ```bash
   streamlit run app.py
   ```

2. **Login:**
   - Usuario: `admin`
   - Contraseña: `Admin1234`

3. **Prueba flujos:**
   - Crea un área
   - Crea una plantilla
   - Crea un usuario operador
   - Logout y login como operador
   - Llena un formulario
   - Vuelve a admin y revisa el envío

Si todo funciona, ¡instalación completa! 🎉

---

## 📚 Documentación Adicional

- [FUNCIONALIDADES.md](./FUNCIONALIDADES.md) - Lista de características
- [CAMBIOS_IMPLEMENTADOS.md](./CAMBIOS_IMPLEMENTADOS.md) - Cambios recientes
- [README.md](./README.md) - Información general

---

**Última actualización:** 19 de Noviembre, 2025
