#!/bin/bash

set -e

echo "🚀 Iniciando Red Social IFTS en CapRover..."

echo "⏳ Verificando conexión a la base de datos..."
python manage.py check --database default

echo "🔄 Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

echo "👤 Verificando superusuario..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@redifts.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    User.objects.create_superuser(
        username=username, 
        email=email, 
        password=password,
        first_name='Administrator',
        last_name='System'
    )
    print(f'✅ Superusuario {username} creado exitosamente')
else:
    print('ℹ️ Superusuario ya existe')
"

echo "📊 Creando datos de ejemplo..."
if [ -f "crear_datos_ejemplo.py" ]; then
    python crear_datos_ejemplo.py
    echo "✅ Datos de ejemplo creados exitosamente"
else
    echo "⚠️ Archivo crear_datos_ejemplo.py no encontrado"
fi

echo "📦 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "📁 Configurando permisos..."
mkdir -p media staticfiles logs
chmod 755 media staticfiles logs

echo "🎉 ¡Configuración completa finalizada!"
echo "🌐 Red Social IFTS lista para usar"
echo "📧 Acceso admin: admin@redifts.com / admin123"
echo "🔗 URL: http://tu-dominio.com/"

echo "🌐 Iniciando servidor web..."
exec gunicorn socialnetwork_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class gthread \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --access-logfile /app/logs/access.log \
    --error-logfile /app/logs/error.log \
    --log-level info