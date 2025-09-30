# Deployment en CapRover - Red Social IFTS

Esta guía te ayudará a desplegar la aplicación de Red Social IFTS en CapRover.

## 📋 Prerrequisitos

- Servidor CapRover configurado y funcionando
- Acceso al dashboard de CapRover
- Git repository con el código fuente

## 🚀 Pasos para el Deployment

### 1. Crear la Aplicación en CapRover

1. Accede al dashboard de CapRover
2. Ve a "Apps" → "One-Click Apps/Databases"
3. Crea una nueva aplicación llamada `social-network-ifts`

### 2. Configurar Variables de Entorno

En la sección "App Configs" → "Environment Variables", configura:

```bash
# Configuración básica
DEBUG=False
DJANGO_SETTINGS_MODULE=socialnetwork_project.production_settings
ALLOWED_HOSTS=*

# Seguridad (CAMBIAR EN PRODUCCIÓN)
SECRET_KEY=tu-clave-secreta-super-segura-aqui-cambiar-en-produccion

# Superusuario inicial
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@ifts.edu.ar
DJANGO_SUPERUSER_PASSWORD=cambiar-en-produccion

# Base de datos (opcional, usa PostgreSQL en producción)
DATABASE_URL=postgres://usuario:password@postgres-host:5432/social_network

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-app
```

### 3. Configurar Volúmenes Persistentes

En "App Configs" → "Persistent Directories":

```
/app/media → /captain/data/media
/app/logs → /captain/data/logs
```

### 4. Desplegar desde Git

1. Ve a "Deployment" → "Deploy via Git"
2. Conecta tu repositorio de GitHub
3. Configura el branch (generalmente `main` o `master`)
4. CapRover detectará automáticamente el `captain-definition` y `Dockerfile`

### 5. Configurar Dominio (Opcional)

1. Ve a "App Configs" → "HTTP Settings"
2. Configura tu dominio personalizado
3. Habilita HTTPS con Let's Encrypt

## 🔧 Configuraciones Avanzadas

### Base de Datos PostgreSQL

Para usar PostgreSQL en lugar de SQLite:

1. Crear una instancia de PostgreSQL en CapRover:
   - Apps → One-Click Apps → PostgreSQL
2. Configurar la variable `DATABASE_URL`:
   ```
   DATABASE_URL=postgres://postgres:password@srv-captain--postgres:5432/social_network
   ```

### Configuración de Email

Para notificaciones por email:

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
```

### Monitoreo y Logs

Los logs se guardan en:

- `/captain/data/logs/django_errors.log` - Errores de Django
- `/captain/data/logs/application_errors.log` - Errores de aplicación

## 📁 Estructura de Archivos

```
proyecto/
├── Dockerfile              # Configuración del contenedor
├── captain-definition       # Configuración de CapRover
├── start.sh                # Script de inicio
├── requirements.txt         # Dependencias Python
├── package.json            # Dependencias Node.js
├── .dockerignore           # Archivos ignorados por Docker
├── socialnetwork_project/
│   ├── settings.py         # Configuración de desarrollo
│   └── production_settings.py  # Configuración de producción
└── ...
```

## 🔍 Troubleshooting

### Problema: Error de migraciones

```bash
# Acceder al contenedor
docker exec -it $(docker ps -q -f name=social-network-ifts) bash

# Ejecutar migraciones manualmente
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### Problema: Archivos estáticos no se cargan

```bash
# Recopilar archivos estáticos
python manage.py collectstatic --noinput --clear
```

### Problema: CSS de Tailwind no se compila

```bash
# Compilar CSS manualmente
npm run build
```

## 🛡️ Consideraciones de Seguridad

1. **Cambiar SECRET_KEY** en producción
2. **Configurar ALLOWED_HOSTS** específicamente
3. **Usar base de datos externa** (PostgreSQL/MySQL)
4. **Configurar HTTPS** con Let's Encrypt
5. **Cambiar credenciales** del superusuario
6. **Configurar copias de seguridad** de la base de datos

## 📚 Comandos Útiles

```bash
# Ver logs en tiempo real
captain logs social-network-ifts

# Reiniciar aplicación
captain restart social-network-ifts

# Escalar aplicación
captain scale social-network-ifts 2

# Ejecutar comando en el contenedor
captain exec social-network-ifts python manage.py shell
```

## 🎯 URLs de la Aplicación

Después del deployment:

- **Home**: `https://tu-dominio.com/main/`
- **Admin**: `https://tu-dominio.com/admin/`
- **Timeline**: `https://tu-dominio.com/main/`

## 📞 Soporte

Si tienes problemas:

1. Revisa los logs en CapRover
2. Verifica las variables de entorno
3. Asegúrate de que todos los volúmenes estén configurados
4. Revisa la conectividad de la base de datos
