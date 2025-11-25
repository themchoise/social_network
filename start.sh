#!/bin/bash

set -e

echo "Iniciando Red Social IFTS en CapRover..."

echo "Verificando conexión a la base de datos..."
python manage.py check --database default

# Solo ejecutar migraciones si la variable SKIP_MIGRATIONS no está establecida
if [ -z "$SKIP_MIGRATIONS" ]; then
  echo "Ejecutando migraciones de base de datos..."
  python manage.py migrate --noinput
else
  echo "⏭️  Saltando migraciones (SKIP_MIGRATIONS=true)"
fi

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Configurando permisos..."
mkdir -p media staticfiles logs
chmod 755 media staticfiles logs

echo "¡Configuración completa finalizada!"
echo "Red Social IFTS lista para usar"
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