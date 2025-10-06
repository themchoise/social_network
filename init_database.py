#!/usr/bin/env python
import os
import django
import sys

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
    
    # 3. Creación de superusuario: siempre manual
    print("ℹ️ La creación automática de superusuario ha sido eliminada. \n"
          "   Para crear un superusuario manualmente, ejecute: python manage.py createsuperuser")
    
    # 4. Carga de datos de ejemplo: siempre manual
    print("La carga automática de datos de ejemplo está deshabilitada.")
    print("Para cargar datos de ejemplo manualmente ejecute: python crear_datos_ejemplo.py")
    
    # 5. Recopilar archivos estáticos
    print("📦 Recopilando archivos estáticos...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("🎉 ¡Configuración completa finalizada!")
    print("🌐 La aplicación está lista para CapRover")
    print("📧 Acceso admin: admin@redifts.com / admin123")

if __name__ == '__main__':
    init_database()