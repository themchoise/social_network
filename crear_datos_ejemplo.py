#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialnetwork_project.settings')
django.setup()

from apps.user.models import User
from apps.career.models import Career

def crear_datos_ejemplo():
    print("Creando datos de ejemplo...")
    
    carreras_data = [
        {
            'name': 'Técnico Superior en Análisis de Sistemas',
            'code': 'TSAS001',
            'description': 'Carrera orientada al análisis y diseño de sistemas de información',
            'duration_years': 3,
            'duration_semesters': 6,
            'total_credits': 180,
            'faculty': 'Instituto de Tecnología'
        },
        {
            'name': 'Técnico Superior en Desarrollo Web',
            'code': 'TSDW002',
            'description': 'Carrera enfocada en el desarrollo de aplicaciones web modernas',
            'duration_years': 2,
            'duration_semesters': 4,
            'total_credits': 120,
            'faculty': 'Instituto de Tecnología'
        },
        {
            'name': 'Técnico Superior en Redes y Seguridad',
            'code': 'TSRS003',
            'description': 'Carrera especializada en administración de redes y ciberseguridad',
            'duration_years': 3,
            'duration_semesters': 6,
            'total_credits': 180,
            'faculty': 'Instituto de Tecnología'
        },
        {
            'name': 'Técnico Superior en Base de Datos',
            'code': 'TSBD004',
            'description': 'Carrera orientada a la administración y desarrollo de bases de datos',
            'duration_years': 2,
            'duration_semesters': 4,
            'total_credits': 120,
            'faculty': 'Instituto de Tecnología'
        },
    ]
    
    carreras_creadas = []
    for carrera_data in carreras_data:
        carrera, created = Career.objects.get_or_create(
            code=carrera_data['code'],
            defaults=carrera_data
        )
        carreras_creadas.append(carrera)
        if created:
            print(f"Carrera creada: {carrera.name}")
        else:
            print(f"Carrera ya existe: {carrera.name}")
    
    usuarios_data = [
        {
            'username': 'juan.perez',
            'email': 'juan@email.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'bio': 'Estudiante apasionado por el análisis de sistemas',
            'student_id': 'ST001',
            'carrera_idx': 0,
            'current_semester': 2
        },
        {
            'username': 'maria.garcia',
            'email': 'maria@email.com',
            'first_name': 'María',
            'last_name': 'García',
            'bio': 'Desarrolladora web frontend especializada en React',
            'student_id': 'ST002',
            'carrera_idx': 1,
            'current_semester': 3
        },
        {
            'username': 'carlos.lopez',
            'email': 'carlos@email.com',
            'first_name': 'Carlos',
            'last_name': 'López',
            'bio': 'Futuro analista de sistemas con interés en UX/UI',
            'student_id': 'ST003',
            'carrera_idx': 0,
            'current_semester': 1
        },
        {
            'username': 'ana.martinez',
            'email': 'ana@email.com',
            'first_name': 'Ana',
            'last_name': 'Martínez',
            'bio': 'Especialista en ciberseguridad y administración de redes',
            'student_id': 'ST004',
            'carrera_idx': 2,
            'current_semester': 4
        },
        {
            'username': 'luis.rodriguez',
            'email': 'luis@email.com',
            'first_name': 'Luis',
            'last_name': 'Rodríguez',
            'bio': 'Desarrollador full-stack con experiencia en Django',
            'student_id': 'ST005',
            'carrera_idx': 1,
            'current_semester': 2
        },
        {
            'username': 'sofia.hernandez',
            'email': 'sofia@email.com',
            'first_name': 'Sofía',
            'last_name': 'Hernández',
            'bio': 'Administradora de bases de datos Oracle y PostgreSQL',
            'student_id': 'ST006',
            'carrera_idx': 3,
            'current_semester': 3
        },
        {
            'username': 'diego.torres',
            'email': 'diego@email.com',
            'first_name': 'Diego',
            'last_name': 'Torres',
            'bio': 'Experto en pentesting y auditorías de seguridad',
            'student_id': 'ST007',
            'carrera_idx': 2,
            'current_semester': 5
        },
        {
            'username': 'admin',
            'email': 'admin@email.com',
            'first_name': 'Admin',
            'last_name': 'System',
            'bio': 'Administrador del sistema',
            'student_id': 'ADM001',
            'carrera_idx': None,
            'current_semester': 1,
            'is_staff': True,
            'is_superuser': True
        },
    ]
    
    for usuario_data in usuarios_data:
        carrera_idx = usuario_data.pop('carrera_idx')
        usuario, created = User.objects.get_or_create(
            username=usuario_data['username'],
            defaults={
                **usuario_data,
                'career': carreras_creadas[carrera_idx] if carrera_idx is not None else None,
                'enrollment_year': 2023,
                'total_points': 50,
                'level': 1
            }
        )
        
        if created:
            usuario.set_password('password123')
            usuario.save()
            print(f"Usuario creado: {usuario.username}")
        else:
            print(f"Usuario ya existe: {usuario.username}")
    
    print("\nResumen de datos creados:")
    print(f"Usuarios totales: {User.objects.count()}")
    print(f"Carreras totales: {Career.objects.count()}")
    
    print("\nDistribucion por carrera:")
    for carrera in Career.objects.all():
        estudiantes_count = carrera.students.count()
        print(f"   {carrera.acronym}: {estudiantes_count} estudiantes")
    
    print("\nDatos de ejemplo creados exitosamente!")
    print("Ahora puedes visitar:")
    print("   - http://127.0.0.1:8000/ (Pagina principal)")
    print("   - http://127.0.0.1:8000/usuarios/ (Lista de usuarios)")
    print("   - http://127.0.0.1:8000/carreras/ (Lista de carreras)")
    print("   - http://127.0.0.1:8000/api/usuarios/ (API JSON)")
    print("   - http://127.0.0.1:8000/admin/ (Panel de administracion)")
    print("      Usuario: admin | Contrasena: password123")

if __name__ == '__main__':
    crear_datos_ejemplo()
