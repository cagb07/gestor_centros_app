# PRODUCCIÓN - Guía de Despliegue

## 📋 Checklist Pre-Producción

- [ ] Cambiar contraseña admin por defecto
- [ ] Crear usuario admin alternativo
- [ ] Configurar variables de entorno (no secrets.toml)
- [ ] Habilitar SSL/TLS
- [ ] Configurar backups de BD
- [ ] Revisar logs de seguridad
- [ ] Configurar CORS si es necesario
- [ ] Hacer pruebas de carga
- [ ] Documentar procedimiento de recuperación

---

## 🚀 Despliegue en Heroku

### 1. Preparar Aplicación

```bash
# Crear Procfile
echo "web: streamlit run app.py --logger.level=error" > Procfile

# Crear runtime.txt
echo "python-3.11.5" > runtime.txt

# Crear .streamlit/config.toml para producción
mkdir -p .streamlit
cat > .streamlit/config.toml << EOF
[server]
port = ${PORT}
headless = true
runOnSave = false

[client]
showErrorDetails = false

[logger]
level = "error"
EOF
```

### 2. Desplegar en Heroku

```bash
# Login
heroku login

# Crear app
heroku create nombre-app-gestor

# Configurar variable de entorno
heroku config:set DB_URL="postgresql://..."

# Desplegar
git push heroku main

# Ver logs
heroku logs --tail
```

---

## 🐳 Despliegue con Docker

### 1. Crear Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Crear docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - DB_URL=${DB_URL}
    volumes:
      - .streamlit:/app/.streamlit
    restart: unless-stopped
```

### 3. Ejecutar

```bash
docker-compose up -d
```

---

## 🔒 Configuración de Seguridad

### Variables de Entorno

**En lugar de `.streamlit/secrets.toml`:**

```bash
# Linux/Mac
export DB_URL="postgresql://..."
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_CLIENT_SHOWERRORDETAILS=false

# Windows
setx DB_URL "postgresql://..."
```

### SSL/TLS con Nginx

```nginx
server {
    listen 443 ssl http2;
    server_name tu-dominio.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 💾 Estrategia de Backups (Neon)

### Backup Manual

```bash
# Exportar BD completa
pg_dump "$DB_URL" > backup.sql

# Restaurar desde backup
psql "$DB_URL" < backup.sql
```

### Backup Automático (Neon)

- Panel de Neon → Backups
- Activa "Automated Backups"
- Configura retención (7, 14, 30 días)

---

## 📊 Monitoreo

### Logs de Aplicación

```bash
# Ver logs en tiempo real
docker logs -f nombre-contenedor

# O en Heroku
heroku logs --tail
```

### Alerts de BD (Neon)

- Configura alertas en Neon
- CPU > 80%
- Conexiones activas > límite
- Storage > 90%

---

## 🔄 Actualización a Nueva Versión

```bash
# 1. Hacer backup
pg_dump "$DB_URL" > backup_pre_upgrade.sql

# 2. Descargar cambios
git pull origin main

# 3. Actualizar dependencias
pip install -r requirements.txt --upgrade

# 4. Ejecutar migraciones (idempotentes, seguras)
python init_db.py

# 5. Reiniciar app
# (Docker: docker-compose restart)
# (Heroku: heroku restart)
```

---

## ⚠️ Notas Importantes

1. **Nunca** commits `secrets.toml`
2. **Siempre** usa SSL/TLS en producción
3. **Siempre** ten backups de BD
4. **Monitorea** consumo de recursos
5. **Cambia** contraseña admin regularmente
6. **Audita** accesos a envíos sensibles
7. **Documenta** todos los cambios
8. **Prueba** antes de desplegar en vivo

---

**Última actualización:** 19 de Noviembre, 2025
