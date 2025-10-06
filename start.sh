#!/bin/bash

set -e

echo "Iniciando Red Social IFTS en CapRover..."

echo "Verificando conexión a la base de datos..."
python manage.py check --database default

echo "Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

echo "La creación de superusuario está deshabilitada en automatización."
echo "   Para crear manualmente un superusuario, ejecute:"
echo "     python manage.py createsuperuser"
echo "   O establezca las variables de entorno y cree manualmente con el comando anterior si lo desea."

echo "Carga de datos de ejemplo deshabilitada en automatización."
echo "Para cargar datos de ejemplo manualmente ejecute:"
echo "  python crear_datos_ejemplo.py"

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Configurando permisos..."
mkdir -p media staticfiles logs
chmod 755 media staticfiles logs

echo "¡Configuración completa finalizada!"
echo "Red Social IFTS lista para usar"
echo "Acceso admin: admin@redifts.com / admin123"
echo "URL: http://tu-dominio.com/"

echo "Iniciando servidor web..."
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