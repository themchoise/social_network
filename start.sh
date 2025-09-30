#!/bin/bash

# Script de inicio para producción en CapRover
set -e

echo "🚀 Iniciando aplicación Django en CapRover..."

# Esperar a que la base de datos esté disponible (si usa PostgreSQL)
echo "⏳ Verificando conexión a la base de datos..."
python manage.py check --database default

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

# Crear superusuario si no existe (usando variables de entorno)
echo "👤 Verificando superusuario..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@ifts.edu.ar')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superusuario {username} creado exitosamente')
else:
    print('Superusuario ya existe')
"

# Recopilar archivos estáticos
echo "📦 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "✅ Configuración completada. Iniciando servidor..."

# Iniciar servidor Gunicorn
exec gunicorn socialnetwork_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 60 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile - \
    --error-logfile - \
    --log-level info