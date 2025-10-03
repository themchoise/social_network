# 🚀 Despliegue Red Social IFTS en CapRover

## 📋 Configuración Automática

Este proyecto está configurado para desplegarse automáticamente en CapRover con todas las dependencias y datos de ejemplo.

### 🛠 Lo que se configura automáticamente:

- ✅ **Base de datos**: Migraciones automáticas
- ✅ **Superusuario**: admin@redifts.com / admin123
- ✅ **Datos de ejemplo**: Usuarios, posts, comentarios, etc.
- ✅ **Archivos estáticos**: CSS compilado con Tailwind
- ✅ **Servidor web**: Gunicorn optimizado
- ✅ **Logs**: Configuración de logging en producción

## 🚀 Pasos para Desplegar

### 1. En CapRover Dashboard:

1. **Crear nueva aplicación**:

   - Nombre: `red-social-ifts`
   - Puerto: `8000`

2. **Configurar variables de entorno** (opcional):

   ```
   DEBUG=False
   SECRET_KEY=tu-clave-secreta-segura
   DATABASE_URL=sqlite:///app/db.sqlite3
   ALLOWED_HOSTS=tu-dominio.com,*.caprover.local
   ```

3. **Configurar dominio personalizado** (opcional):
   - Habilitar HTTPS si está disponible
   - Configurar certificados SSL

### 2. Despliegue desde Git:

1. **Conectar repositorio Git**:

   - URL del repositorio
   - Branch: `main` o `master`

2. **Deploy automático**:
   - CapRover detectará el `captain-definition`
   - Construirá la imagen Docker
   - Ejecutará el contenedor

### 3. Primer acceso:

- **URL de la aplicación**: `https://red-social-ifts.tu-servidor.com`
- **Panel de administración**: `/admin/`
- **Credenciales admin**:
  - Email: `admin@redifts.com`
  - Password: `admin123`

## 📊 Datos de Ejemplo Incluidos

El sistema crea automáticamente:

- **Usuarios**: Estudiantes, profesores, coordinadores
- **Carreras**: Desarrollo Web, Análisis de Sistemas, etc.
- **Materias**: Por carrera con profesores asignados
- **Posts**: Contenido de ejemplo en el timeline
- **Comentarios**: Interacciones entre usuarios
- **Amistades**: Conexiones entre usuarios

## 🔧 Configuración Avanzada

### Variables de Entorno Opcionales:

```bash
# Base de datos PostgreSQL (recomendado para producción)
DATABASE_URL=postgres://user:pass@host:port/dbname

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password

# HTTPS (si está configurado en CapRover)
USE_HTTPS=True
```

### Volúmenes Persistentes:

- `/app/media`: Archivos subidos por usuarios
- `/app/logs`: Logs de la aplicación
- `/app/staticfiles`: Archivos estáticos compilados

## 🐛 Troubleshooting

### Ver logs de la aplicación:

```bash
# En CapRover terminal
tail -f /captain/data/logs/django.log
tail -f /captain/data/logs/access.log
tail -f /captain/data/logs/error.log
```

### Reiniciar la aplicación:

```bash
# En CapRover dashboard: App Settings > Restart App
```

### Ejecutar comandos Django:

```bash
# En CapRover terminal
python manage.py shell
python manage.py createsuperuser
python manage.py collectstatic
```

## 📱 Características de la Aplicación

- **Timeline social**: Posts con likes y comentarios
- **Sistema de amistades**: Solicitudes y conexiones
- **Perfiles de usuario**: Con fotos y información académica
- **Grupos académicos**: Por carrera y materia
- **Notificaciones**: En tiempo real
- **Panel de administración**: Gestión completa
- **Responsive**: Optimizado para móviles

## 🔒 Seguridad

- HTTPS recomendado en producción
- Cambiar `SECRET_KEY` en producción
- Configurar `ALLOWED_HOSTS` específicos
- Usar PostgreSQL para producción
- Configurar backups regulares

## 📞 Soporte

Para problemas o dudas:

- Revisar logs en `/captain/data/logs/`
- Verificar variables de entorno
- Reiniciar la aplicación si es necesario

---

🎉 **¡Tu Red Social IFTS está lista para usar!** 🎉
