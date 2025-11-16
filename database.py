import streamlit as st
import psycopg2
import pandas as pd
import json
import os

# --- CONEXIÓN PRINCIPAL ---

@st.cache_resource
def get_db_connection():
    """
    Se conecta a la base de datos Postgres.
    Intenta leer de st.secrets primero, luego de variables de entorno.
    """
    db_url = None
    
    # 1. Intentar leer de secretos de Streamlit (cuando la app corre)
    try:
        if "DB_URL" in st.secrets:
            db_url = st.secrets["DB_URL"]
    except Exception:
        pass # st.secrets no existe en el script init_db
    
    # 2. Si falla, intentar leer de variables de entorno (para init_db.py)
    if not db_url:
        db_url = os.environ.get("DB_URL")

    if not db_url:
        # Si estamos en un script (como init_db), esto lanzará un error
        # Si estamos en Streamlit, mostrará el error en la app
        st.error("❌ Error: No se encontró DB_URL en secrets.toml ni en variables de entorno.")
        st.stop()

    # Dejamos que el error se propague si la conexión falla
    conn = psycopg2.connect(db_url)
    return conn

# --- INICIALIZACIÓN ---

def create_tables():
    """Crea todas las tablas de la app si no existen."""
    conn = get_db_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            # Tabla de Áreas
            cur.execute("""
                CREATE TABLE IF NOT EXISTS form_areas (
                    id SERIAL PRIMARY KEY,
                    area_name VARCHAR(100) UNIQUE NOT NULL,
                    description TEXT
                );
            """)
            
            # Tabla de Usuarios
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash BYTEA NOT NULL,
                    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'operador')),
                    full_name VARCHAR(100)
                );
            """)
            
            # Tabla de Plantillas
            cur.execute("""
                CREATE TABLE IF NOT EXISTS form_templates (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    structure JSONB NOT NULL,
                    created_by_user_id INTEGER REFERENCES usuarios(id),
                    area_id INTEGER REFERENCES form_areas(id)
                );
            """)
            
            # Tabla de Envíos
            cur.execute("""
                CREATE TABLE IF NOT EXISTS form_submissions (
                    id SERIAL PRIMARY KEY,
                    template_id INTEGER REFERENCES form_templates(id),
                    user_id INTEGER REFERENCES usuarios(id),
                    data JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()
        print("✅ Tablas verificadas/creadas exitosamente.")
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
    # NOTA: NO HAY 'conn.close()' AQUÍ. ES INTENCIONAL.

# --- FUNCIONES DE USUARIO ---

def get_user(username):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, username, password_hash, role, full_name FROM usuarios WHERE username = %s", (username,))
        user_data = cur.fetchone()
    # Sin conn.close()
    if user_data:
        return {"id": user_data[0], "username": user_data[1], "password_hash": user_data[2], "role": user_data[3], "full_name": user_data[4]}
    return None

def create_admin_user(username, password, full_name):
    from auth import hash_password
    hashed = hash_password(password)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO usuarios (username, password_hash, role, full_name) VALUES (%s, %s, 'admin', %s)", (username, hashed, full_name))
        conn.commit()
        print(f"✅ Usuario admin '{username}' creado.")
    except psycopg2.IntegrityError:
        print(f"⚠️  Usuario admin '{username}' ya existe. No se creó de nuevo.")
    except Exception as e:
        print(f"❌ Error creando admin: {e}")
    # Sin conn.close()

def create_user(username, password, role, full_name):
    from auth import hash_password
    hashed = hash_password(password)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO usuarios (username, password_hash, role, full_name) VALUES (%s, %s, %s, %s)", (username, hashed, role, full_name))
        conn.commit()
        return True, "Usuario creado."
    except psycopg2.IntegrityError:
        conn.rollback()
        return False, "El usuario ya existe."
    # Sin conn.close()

def get_all_users():
    conn = get_db_connection()
    df = pd.read_sql("SELECT id, username, role, full_name FROM usuarios ORDER BY full_name", conn)
    # Sin conn.close()
    return df

# --- FUNCIONES DE ÁREAS Y TEMPLATES ---

def create_area(area_name, description):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO form_areas (area_name, description) VALUES (%s, %s)", (area_name, description))
        conn.commit()
        return True, "Área creada."
    except psycopg2.IntegrityError:
        conn.rollback()
        return False, "El nombre de área ya existe."
    # Sin conn.close()

def get_all_areas():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, area_name, description FROM form_areas ORDER BY area_name")
        data = [{"id": a[0], "name": a[1], "description": a[2]} for a in cur.fetchall()]
    # Sin conn.close()
    return data

def save_form_template(name, structure, user_id, area_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO form_templates (name, structure, created_by_user_id, area_id) VALUES (%s, %s, %s, %s)", 
                    (name, json.dumps(structure), user_id, area_id))
    conn.commit()
    # Sin conn.close()

def get_templates_by_area(area_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM form_templates WHERE area_id = %s ORDER BY name", (area_id,))
        data = [{"id": t[0], "name": t[1]} for t in cur.fetchall()]
    # Sin conn.close()
    return data

def get_template_structure(template_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT structure FROM form_templates WHERE id = %s", (template_id,))
        res = cur.fetchone()
    # Sin conn.close()
    return res[0] if res else None

# --- FUNCIONES DE ENVÍOS Y DASHBOARD ---

def save_submission(template_id, user_id, data):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO form_submissions (template_id, user_id, data) VALUES (%s, %s, %s)", 
                    (template_id, user_id, json.dumps(data, default=str)))
    conn.commit()
    # Sin conn.close()

def get_submissions_by_user(user_id):
    conn = get_db_connection()
    df = pd.read_sql("""
        SELECT s.id, t.name, s.created_at, s.data FROM form_submissions s 
        JOIN form_templates t ON s.template_id = t.id WHERE s.user_id = %s ORDER BY s.created_at DESC
    """, conn, params=(user_id,))