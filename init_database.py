#!/usr/bin/env python
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialnetwork_project.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from django.db import connection

def init_database():
    """Inicializar base de datos completa"""
    
    print("🚀 Iniciando configuración completa de la base de datos...")
    
    # 1. Crear migraciones
    print("📝 Creando migraciones...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # 2. Aplicar migraciones
    print("⚡ Aplicando migraciones...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # 3. Crear superusuario si no existe
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        print("👤 Creando superusuario admin...")
        User.objects.create_superuser(
            username='admin',
            email='admin@redifts.com',
            password='admin123',
            first_name='Administrator',
            last_name='System'
        )
        print("✅ Superusuario creado: admin/admin123")
    
    # 4. Crear datos de ejemplo
    print("📊 Creando datos de ejemplo...")
    import subprocess
    result = subprocess.run([sys.executable, 'crear_datos_ejemplo.py'], 
                          capture_output=True, text=True, cwd='/app')
    if result.returncode == 0:
        print("✅ Datos de ejemplo creados exitosamente")
    else:
        print(f"⚠️ Error creando datos: {result.stderr}")
    
    # 5. Recopilar archivos estáticos
    print("📦 Recopilando archivos estáticos...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("🎉 ¡Configuración completa finalizada!")
    print("🌐 La aplicación está lista para CapRover")
    print("📧 Acceso admin: admin@redifts.com / admin123")

if __name__ == '__main__':
    init_database()