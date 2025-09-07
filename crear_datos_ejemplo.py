#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialnetwork_project.settings')
django.setup()

from django.contrib.auth.models import User
from apps.usuario.models import PerfilUsuario, Carrera

def crear_datos_ejemplo():
    print("🚀 Creando datos de ejemplo...")
    
    carreras_data = [
        {'nombre': 'Técnico Superior en Análisis de Sistemas', 'acronmico': 'TSAS'},
        {'nombre': 'Técnico Superior en Desarrollo Web', 'acronmico': 'TSDW'},
        {'nombre': 'Técnico Superior en Redes y Seguridad', 'acronmico': 'TSRS'},
        {'nombre': 'Técnico Superior en Base de Datos', 'acronmico': 'TSBD'},
    ]
    
    carreras_creadas = []
    for carrera_data in carreras_data:
        carrera, created = Carrera.objects.get_or_create(
            acronmico=carrera_data['acronmico'],
            defaults={'nombre': carrera_data['nombre']}
        )
        carreras_creadas.append(carrera)
        if created:
            print(f"✅ Carrera creada: {carrera.nombre}")
        else:
            print(f"ℹ️  Carrera ya existe: {carrera.nombre}")
    
    usuarios_data = [
        {'username': 'juan.perez', 'email': 'juan@email.com', 'first_name': 'Juan', 'last_name': 'Pérez', 'nombre_perfil': 'Juan Carlos Pérez', 'carrera_idx': 0},
        {'username': 'maria.garcia', 'email': 'maria@email.com', 'first_name': 'María', 'last_name': 'García', 'nombre_perfil': 'María Elena García', 'carrera_idx': 1},
        {'username': 'carlos.lopez', 'email': 'carlos@email.com', 'first_name': 'Carlos', 'last_name': 'López', 'nombre_perfil': 'Carlos Daniel López', 'carrera_idx': 0},
        {'username': 'ana.martinez', 'email': 'ana@email.com', 'first_name': 'Ana', 'last_name': 'Martínez', 'nombre_perfil': 'Ana Lucía Martínez', 'carrera_idx': 2},
        {'username': 'luis.rodriguez', 'email': 'luis@email.com', 'first_name': 'Luis', 'last_name': 'Rodríguez', 'nombre_perfil': 'Luis Fernando Rodríguez', 'carrera_idx': 1},
        {'username': 'sofia.hernandez', 'email': 'sofia@email.com', 'first_name': 'Sofía', 'last_name': 'Hernández', 'nombre_perfil': 'Sofía Isabel Hernández', 'carrera_idx': 3},
        {'username': 'diego.torres', 'email': 'diego@email.com', 'first_name': 'Diego', 'last_name': 'Torres', 'nombre_perfil': 'Diego Alejandro Torres', 'carrera_idx': 2},
        {'username': 'usuario.sin.carrera', 'email': 'sincarrera@email.com', 'first_name': 'Usuario', 'last_name': 'Sin Carrera', 'nombre_perfil': 'Usuario Sin Carrera Asignada', 'carrera_idx': None},
    ]
    
    for usuario_data in usuarios_data:
        usuario, created = User.objects.get_or_create(
            username=usuario_data['username'],
            defaults={
                'email': usuario_data['email'],
                'first_name': usuario_data['first_name'],
                'last_name': usuario_data['last_name'],
            }
        )
        
        if created:
            print(f"✅ Usuario creado: {usuario.username}")
        else:
            print(f"ℹ️  Usuario ya existe: {usuario.username}")
        
        perfil, perfil_created = PerfilUsuario.objects.get_or_create(
            usuario=usuario,
            defaults={
                'nombre': usuario_data['nombre_perfil'],
                'carrera': carreras_creadas[usuario_data['carrera_idx']] if usuario_data['carrera_idx'] is not None else None
            }
        )
        
        if perfil_created:
            print(f"✅ Perfil creado para: {usuario.username}")
        else:
            print(f"ℹ️  Perfil ya existe para: {usuario.username}")
    
    print("\n📊 Resumen de datos creados:")
    print(f"👥 Usuarios totales: {User.objects.count()}")
    print(f"📝 Perfiles totales: {PerfilUsuario.objects.count()}")
    print(f"🎓 Carreras totales: {Carrera.objects.count()}")
    
    print("\n📚 Distribución por carrera:")
    for carrera in Carrera.objects.all():
        estudiantes_count = carrera.estudiantes.count()
        print(f"   {carrera.acronmico}: {estudiantes_count} estudiantes")
    
    print("\n🎉 ¡Datos de ejemplo creados exitosamente!")
    print("🌐 Ahora puedes visitar:")
    print("   - http://127.0.0.1:8000/ (Página principal)")
    print("   - http://127.0.0.1:8000/usuarios/ (Lista de usuarios)")
    print("   - http://127.0.0.1:8000/carreras/ (Lista de carreras)")
    print("   - http://127.0.0.1:8000/api/usuarios/ (API JSON)")

if __name__ == '__main__':
    crear_datos_ejemplo()
