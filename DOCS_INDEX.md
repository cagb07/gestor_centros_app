# 📚 Documentación de la Aplicación - Índice

Esta carpeta contiene la documentación completa para instalar, usar, desplegar y mantener el Gestor de Centros Educativos.

---

## 🚀 Para Empezar Rápido

### 👤 Yo soy un **usuario nuevo** que quiere instalar

**→ Lee:** [`NEW_INSTALLATION.md`](NEW_INSTALLATION.md)

- ✅ Checklist paso a paso
- ✅ Requisitos previos
- ✅ Setup rápido (automático o manual)
- ✅ Configuración BD (Neon o PostgreSQL)
- ✅ Primeros pasos y troubleshooting

**Tiempo estimado:** 30 minutos

---

### 💻 Yo soy un **desarrollador** que quiere entender la app

**→ Lee:** [`README.md`](README.md) + [`FUNCIONALIDADES.md`](FUNCIONALIDADES.md)

- ✅ Descripción general
- ✅ Características principales
- ✅ Flujos de uso
- ✅ Validaciones implementadas
- ✅ Arquitectura (archivos y estructura)

**Tiempo estimado:** 15 minutos

---

### 🔧 Yo quiero **instalar en detalle** y entender cada paso

**→ Lee:** [`INSTALL.md`](INSTALL.md)

- ✅ Requisitos previos detallados
- ✅ Setup rápido (automático)
- ✅ Setup manual (para todas las plataformas)
- ✅ Configuración de BD (2 opciones)
- ✅ Verificación de instalación
- ✅ Troubleshooting detallado

**Tiempo estimado:** 45 minutos

---

### 🌍 Yo quiero **desplegar en producción**

**→ Lee:** [`PRODUCTION.md`](PRODUCTION.md)

- ✅ Checklist pre-producción
- ✅ Despliegue en Heroku
- ✅ Despliegue con Docker
- ✅ Seguridad (SSL/TLS, variables de entorno)
- ✅ Backups y monitoreo
- ✅ Actualización de versiones

**Tiempo estimado:** 1-2 horas (dependiendo de la plataforma)

---

### 📋 Yo quiero **ver qué cambios se hicieron** en la última versión

**→ Lee:** [`CAMBIOS_IMPLEMENTADOS.md`](CAMBIOS_IMPLEMENTADOS.md)

- ✅ Resumen de cambios
- ✅ Archivos modificados
- ✅ Nuevas funciones (v2.0)
- ✅ Cambios en BD
- ✅ Cómo probar lo nuevo

**Tiempo estimado:** 10 minutos

---

### 📊 Yo quiero **ver todas las funcionalidades**

**→ Lee:** [`FUNCIONALIDADES.md`](FUNCIONALIDADES.md)

- ✅ Dashboard Admin
- ✅ Panel Operador
- ✅ Validaciones implementadas
- ✅ Mejoras UX/UI
- ✅ Características técnicas
- ✅ Próximas mejoras sugeridas

**Tiempo estimado:** 15 minutos

---

## 📖 Documentos Completos

### 1. **NEW_INSTALLATION.md** 📦
Guía paso a paso para instalación nueva (recomendado para nuevos usuarios)
- Fases 1-7 (Requisitos → Primeros Pasos)
- Troubleshooting rápido
- Checklist final

### 2. **INSTALL.md** 🔧
Documentación de instalación completa y detallada
- Setup rápido (automático con script)
- Setup manual (todos los OS)
- Configuración Neon vs PostgreSQL Local
- Verificación de instalación
- Troubleshooting extenso

### 3. **README.md** 📖
Información general de la aplicación
- Características principales
- Inicio rápido (5 min)
- Credenciales por defecto
- Flujos de uso principales
- Estructura del proyecto
- Seguridad
- FAQ

### 4. **FUNCIONALIDADES.md** 📊
Descripción detallada de todas las características
- Panel Admin (6 pestañas)
- Panel Operador (3 pestañas)
- Validaciones
- Mejoras UX/UI
- Nuevas características v2.0 (auditoría)

### 5. **CAMBIOS_IMPLEMENTADOS.md** 🔄
Documentación de cambios en la versión 2.0
- Resumen de cambios
- Cambios BD (DROP eliminado, columnas review)
- Nuevo archivo `db_helpers.py`
- Cambios en `admin_view.py`
- Cambios en tests
- Cómo probar

### 6. **PRODUCTION.md** 🚀
Guía de despliegue en producción
- Checklist pre-producción
- Heroku (Procfile, setup)
- Docker (Dockerfile, docker-compose)
- Seguridad (variables de entorno, SSL)
- Backups y monitoreo
- Actualización de versiones

---

## 🛠️ Scripts de Utilidad

### `setup.sh` (Linux/Mac)
```bash
chmod +x setup.sh
./setup.sh
```
Automatiza toda la instalación (venv, dependencias, secrets, init_db)

### `verify_installation.py`
```bash
python verify_installation.py
```
Verifica que todos los componentes están correctamente configurados

### `init_db.py`
```bash
python init_db.py
```
Inicializa la base de datos (crear tablas, usuario admin)

---

## 🔍 Búsqueda Rápida de Soluciones

### Tengo problema con...

| Problema | Documento | Sección |
|----------|-----------|---------|
| No sé por dónde empezar | [`NEW_INSTALLATION.md`](NEW_INSTALLATION.md) | Inicio |
| Python/Git no instalados | [`NEW_INSTALLATION.md`](NEW_INSTALLATION.md) | FASE 1 |
| Tengo error en setup | [`INSTALL.md`](INSTALL.md) | Troubleshooting |
| Neon: qué hacer con IP Allow List | [`INSTALL.md`](INSTALL.md) | Configuración Neon |
| PostgreSQL local no funciona | [`INSTALL.md`](INSTALL.md) | Configuración Local |
| Error de conexión a BD | [`INSTALL.md`](INSTALL.md) | Troubleshooting |
| Quiero desplegar a producción | [`PRODUCTION.md`](PRODUCTION.md) | Inicio |
| Tengo Heroku pero no sé cómo | [`PRODUCTION.md`](PRODUCTION.md) | Heroku |
| Prefiero Docker | [`PRODUCTION.md`](PRODUCTION.md) | Docker |
| Qué cambió en v2.0 | [`CAMBIOS_IMPLEMENTADOS.md`](CAMBIOS_IMPLEMENTADOS.md) | Inicio |

---

## 📋 Estructura de Documentación

```
Documentación/
├── 📦 Instalación
│   ├── NEW_INSTALLATION.md (👈 empezar aquí)
│   ├── INSTALL.md (detallado)
│   └── setup.sh (automatizado)
├── 📖 Referencia
│   ├── README.md
│   ├── FUNCIONALIDADES.md
│   └── CAMBIOS_IMPLEMENTADOS.md
├── 🚀 Despliegue
│   └── PRODUCTION.md
└── 🔍 Verificación
    └── verify_installation.py
```

---

## 🎯 Rutas Recomendadas por Perfil

### 👶 Principiante Total
1. [`NEW_INSTALLATION.md`](NEW_INSTALLATION.md) - FASE 1-7
2. [`README.md`](README.md) - Características
3. Ejecutar app y explorar

### 🎓 Usuario Intermediario
1. [`README.md`](README.md) - General
2. [`FUNCIONALIDADES.md`](FUNCIONALIDADES.md) - Features
3. Ejecutar app
4. [`INSTALL.md`](INSTALL.md) si hay problemas

### 👨‍💻 Desarrollador
1. [`README.md`](README.md) - Arquitectura
2. [`CAMBIOS_IMPLEMENTADOS.md`](CAMBIOS_IMPLEMENTADOS.md) - v2.0
3. Revisar código en `admin_view.py`, `db_helpers.py`
4. [`PRODUCTION.md`](PRODUCTION.md) si va a desplegar

### 🏢 DevOps/Sysadmin
1. [`PRODUCTION.md`](PRODUCTION.md) - Despliegue
2. [`INSTALL.md`](INSTALL.md) - Setup
3. Scripts: `setup.sh`, `verify_installation.py`
4. Configuración de BD (Neon o PostgreSQL)

---

## ⏱️ Tiempos Estimados

| Actividad | Tiempo |
|-----------|--------|
| Lectura rápida (NEW_INSTALLATION) | 10 min |
| Setup automático (setup.sh) | 10 min |
| Setup manual completo | 30 min |
| Primeros pasos y pruebas | 10 min |
| **Total: Instalación** | **~40 min** |
| Lectura PRODUCTION.md | 15 min |
| Despliegue Heroku | 20 min |
| Despliegue Docker | 20 min |
| **Total: Producción** | **~60 min** |

---

## 🔐 Seguridad

⚠️ **IMPORTANTE:**

- [ ] Nunca commitees `.streamlit/secrets.toml`
- [ ] Cambia contraseña admin en primera sesión
- [ ] En producción, usa variables de entorno
- [ ] En producción, habilita SSL/TLS
- [ ] Regularmente respalda la BD
- [ ] Monitorea accesos y cambios

Ver [`PRODUCTION.md`](PRODUCTION.md) para más detalles.

---

## 📞 Soporte Rápido

### El script setup.sh no funciona
→ Lee [`NEW_INSTALLATION.md`](NEW_INSTALLATION.md) **Opción B** (manual)

### No puedo conectar a BD
→ Consulta [`INSTALL.md`](INSTALL.md) **Troubleshooting** → "Error de conexión"

### Quiero que funcione mañana en producción
→ Sigue [`PRODUCTION.md`](PRODUCTION.md) + [`INSTALL.md`](INSTALL.md)

### Necesito entender todo primero
→ Lee [`README.md`](README.md) + [`FUNCIONALIDADES.md`](FUNCIONALIDADES.md)

---

## 📌 Resumen Rápido

**Para instalar:** `NEW_INSTALLATION.md` → `setup.sh` → `verify_installation.py`

**Para usar:** `README.md` → Ejecuta app → Explora

**Para producción:** `PRODUCTION.md` → Choose (Heroku/Docker) → Deploy

**Para debugging:** `INSTALL.md` → Troubleshooting

---

**Última actualización:** 19 de Noviembre, 2025
**Versión:** 2.0 con documentación completa
