#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialnetwork_project.settings')
django.setup()

from apps.user.models import User
from apps.career.models import Career
from apps.subject.models import Subject
from apps.achievement.models import Achievement, UserAchievement
from apps.post.models import Post
from apps.comment.models import Comment
from apps.note.models import Note
from apps.group.models import Group, GroupMembership
from apps.friendship.models import Friendship


def crear_carreras():
    print("Creando carreras...")
    
    carreras_data = [
        {
            'name': 'Tecnico Superior en Analisis de Sistemas (2007)',
            'code': 'TSAS2007',
            'acronym': 'TSAS07',
            'description': 'Carrera orientada al analisis y diseno de sistemas de informacion - Plan 2007',
            'duration_years': 3,
            'duration_semesters': 6,
            'total_credits': 180,
            'faculty': 'Instituto de Tecnologia',
            'career_type': 'technical'
        },
        {
            'name': 'Tecnico Superior en Analisis de Sistemas (2024)',
            'code': 'TSAS2024',
            'acronym': 'TSAS24',
            'description': 'Carrera orientada al analisis y diseno de sistemas de informacion - Plan 2024 actualizado',
            'duration_years': 3,
            'duration_semesters': 6,
            'total_credits': 180,
            'faculty': 'Instituto de Tecnologia',
            'career_type': 'technical'
        },
        {
            'name': 'Tecnico Superior en Desarrollo de Software',
            'code': 'TSDS2024',
            'acronym': 'TSDS',
            'description': 'Carrera enfocada en el desarrollo integral de software moderno',
            'duration_years': 3,
            'duration_semesters': 6,
            'total_credits': 180,
            'faculty': 'Instituto de Tecnologia',
            'career_type': 'technical'
        },
        {
            'name': 'Tecnico Superior en Ciencia de Datos e Inteligencia Artificial',
            'code': 'TSCDAI2024',
            'acronym': 'TSCDAI',
            'description': 'Carrera especializada en ciencia de datos, machine learning e inteligencia artificial',
            'duration_years': 3,
            'duration_semesters': 6,
            'total_credits': 180,
            'faculty': 'Instituto de Tecnologia',
            'career_type': 'technical'
        }
    ]
    
    carreras_creadas = {}
    for carrera_data in carreras_data:
        carrera, created = Career.objects.get_or_create(
            code=carrera_data['code'],
            defaults=carrera_data
        )
        carreras_creadas[carrera_data['acronym']] = carrera
        if created:
            print(f"Carrera creada: {carrera.name}")
        else:
            print(f"Carrera ya existe: {carrera.name}")
    
    return carreras_creadas


def crear_materias(carreras):
    print("Creando materias para TSDS...")
    
    carrera_tsds = carreras.get('TSDS')
    if not carrera_tsds:
        print("Error: No se encontro la carrera TSDS")
        return {}
    
    materias_data = [
        {
            'name': 'Tecnicas de Programacion',
            'code': '1.1.1',
            'semester': 1,
            'credits': 9,
            'subject_type': 'mandatory',
            'description': 'Fundamentos de programacion y algoritmos'
        },
        {
            'name': 'Administracion de Base de Datos',
            'code': '1.1.2', 
            'semester': 1,
            'credits': 9,
            'subject_type': 'mandatory',
            'description': 'Fundamentos de bases de datos relacionales'
        },
        {
            'name': 'Elementos de Analisis Matematico',
            'code': '1.1.3',
            'semester': 1,
            'credits': 6,
            'subject_type': 'mandatory',
            'description': 'Matematica aplicada al desarrollo de software'
        },
        {
            'name': 'Logica Computacional',
            'code': '1.1.4',
            'semester': 1,
            'credits': 6,
            'subject_type': 'mandatory',
            'description': 'Logica matematica y computacional'
        },
        {
            'name': 'Desarrollo de Sistemas Orientados a Objetos',
            'code': '1.2.1',
            'semester': 2,
            'credits': 9,
            'subject_type': 'mandatory',
            'description': 'Programacion orientada a objetos avanzada',
            'prerequisites': ['1.1.1', '1.1.2', '1.1.4']
        },
        {
            'name': 'Modelado y Diseno de Software',
            'code': '1.2.2',
            'semester': 2,
            'credits': 3,
            'subject_type': 'mandatory',
            'description': 'UML y patrones de diseno',
            'prerequisites': ['1.1.1']
        },
        {
            'name': 'Estadistica y Probabilidad para el Desarrollo de Software',
            'code': '1.2.3',
            'semester': 2,
            'credits': 6,
            'subject_type': 'mandatory',
            'description': 'Estadistica aplicada al desarrollo'
        },
        {
            'name': 'Ingles',
            'code': '1.2.4',
            'semester': 2,
            'credits': 6,
            'subject_type': 'mandatory',
            'description': 'Ingles tecnico para desarrollo de software'
        },
        {
            'name': 'Practica Profesional I (Aproximacion al mundo laboral)',
            'code': '1.2.5',
            'semester': 2,
            'credits': 6,
            'subject_type': 'mandatory',
            'description': 'Primera aproximacion al mundo laboral'
        },
        {
            'name': 'Desarrollo de Aplicaciones para Dispositivos Moviles',
            'code': '2.1.1',
            'semester': 3,
            'credits': 9,
            'subject_type': 'mandatory',
            'description': 'Desarrollo mobile multiplataforma',
            'prerequisites': ['1.2.1', '1.2.2']
        },
        {
            'name': 'Metodologia de Prueba de Sistemas',
            'code': '2.1.2',
            'semester': 3,
            'credits': 9,
            'subject_type': 'mandatory',
            'description': 'Testing y QA de software',
            'prerequisites': ['1.1.1']
        },
        {
            'name': 'Tecnologias de la Informacion y de la Comunicacion',
            'code': '2.1.3',
            'semester': 3,
            'credits': 3,
            'subject_type': 'mandatory',
            'description': 'TIC aplicadas al desarrollo'
        },
        {
            'name': 'Taller de Comunicacion',
            'code': '2.1.4',
            'semester': 3,
            'credits': 3,
            'subject_type': 'mandatory',
            'description': 'Comunicacion efectiva en equipos de desarrollo'
        },
        {
            'name': 'Desarrollo de Sistemas de Informacion Orientados a la Gestion y Apoyo a las Decisiones',
            'code': '2.1.5',
            'semester': 3,
            'credits': 6,
            'subject_type': 'mandatory',
            'description': 'Sistemas de informacion gerencial',
            'prerequisites': ['1.2.1', '1.2.2', '1.2.5']
        },
        {
            'name': 'Desarrollo de Sistemas Web (Back End)',
            'code': '2.2.1',
            'semester': 4,
            'credits': 9,
            'subject_type': 'mandatory',
            'description': 'Desarrollo backend con frameworks modernos',
            'prerequisites': ['2.1.1', '2.1.2', '2.1.3']
        },
        {
            'name': 'Desarrollo de Sistemas Web (Front End)',
            'code': '2.2.2',
            'semester': 4,
            'credits': 3,
            'subject_type': 'mandatory',
            'description': 'Desarrollo frontend moderno',
            'prerequisites': ['1.2.2']
        },
        {
            'name': 'Ingenieria de Software',
            'code': '2.2.3',
            'semester': 4,
            'credits': 9,
            'subject_type': 'mandatory',
            'description': 'Metodologias agiles y gestion de proyectos'
        },
        {
            'name': 'Desarrollo e Implementacion de Sistemas en la Nube',
            'code': '2.2.4',
            'semester': 4,
            'credits': 9,
            'subject_type': 'mandatory',
            'description': 'Cloud computing y DevOps',
            'prerequisites': ['2.1.1', '2.1.3', '2.1.5']
        },
        {
            'name': 'Programacion sobre Redes',
            'code': '3.1.1',
            'semester': 5,
            'credits': 9,
            'subject_type': 'mandatory',
            'description': 'Programacion de aplicaciones distribuidas',
            'prerequisites': ['2.2.1', '2.2.3']
        },
        {
            'name': 'Seminario de Profundizacion y/o Actualizacion',
            'code': '3.1.2',
            'semester': 5,
            'credits': 3,
            'subject_type': 'elective',
            'description': 'Seminarios de tecnologias emergentes',
            'prerequisites': ['2.2.3']
        },
        {
            'name': 'Gestion de Proyectos',
            'code': '3.1.3',
            'semester': 5,
            'credits': 6,
            'subject_type': 'mandatory',
            'description': 'Gestion integral de proyectos de software',
            'prerequisites': ['2.2.3']
        },
        {
            'name': 'Trabajo, Tecnologia y Sociedad',
            'code': '3.1.4',
            'semester': 5,
            'credits': 3,
            'subject_type': 'mandatory',
            'description': 'Impacto social de la tecnologia'
        },
        {
            'name': 'Proyecto Integrador',
            'code': '3.1.5',
            'semester': 5,
            'credits': 12,
            'subject_type': 'mandatory',
            'description': 'Proyecto final integrador'
        }
    ]
    
    materias_creadas = {}
    prerequisitos_pendientes = []
    
    for materia_data in materias_data:
        prerequisites = materia_data.pop('prerequisites', [])
        
        materia, created = Subject.objects.get_or_create(
            code=materia_data['code'],
            defaults=materia_data
        )
        
        materia.career.add(carrera_tsds)
        
        materias_creadas[materia_data['code']] = materia
        
        if prerequisites:
            prerequisitos_pendientes.append((materia, prerequisites))
        
        if created:
            print(f"Materia creada: {materia.name}")
        else:
            print(f"Materia ya existe: {materia.name}")
    
    print("Asignando prerequisitos...")
    for materia, prerequisitos in prerequisitos_pendientes:
        for prereq_code in prerequisitos:
            if prereq_code in materias_creadas:
                materia.prerequisites.add(materias_creadas[prereq_code])
                print(f"   {materia.code} -> prerequisito: {prereq_code}")
    
    return materias_creadas


def crear_usuarios_avanzados(carreras):
    print("Creando usuarios avanzados...")
    
    usuarios_data = [
        {
            'username': 'prof.garcia',
            'email': 'garcia@instituto.edu.ar',
            'first_name': 'Maria',
            'last_name': 'Garcia',
            'bio': 'Profesora de Programacion y Desarrollo de Software. 15 anos de experiencia en la industria.',
            'student_id': 'PROF001',
            'career': 'TSDS',
            'current_semester': 1,
            'is_staff': True,
            'is_mentor': True,
            'total_points': 1500,
            'level': 5
        },
        {
            'username': 'est.rodriguez',
            'email': 'rodriguez@estudiante.edu.ar',
            'first_name': 'Carlos',
            'last_name': 'Rodriguez',
            'bio': 'Estudiante de 2do ano, apasionado por el desarrollo web y mobile.',
            'student_id': 'EST001',
            'career': 'TSDS',
            'current_semester': 3,
            'total_points': 750,
            'level': 3
        },
        {
            'username': 'ana.sistemas',
            'email': 'ana@estudiante.edu.ar',
            'first_name': 'Ana',
            'last_name': 'Martinez',
            'bio': 'Estudiante de Analisis de Sistemas, plan 2024. Interesada en IA.',
            'student_id': 'EST002',
            'career': 'TSAS24',
            'current_semester': 2,
            'total_points': 400,
            'level': 2
        },
        {
            'username': 'luis.datos',
            'email': 'luis@estudiante.edu.ar',
            'first_name': 'Luis',
            'last_name': 'Fernandez',
            'bio': 'Futuro cientifico de datos, me encanta Python y Machine Learning.',
            'student_id': 'EST003',
            'career': 'TSCDAI',
            'current_semester': 1,
            'total_points': 200,
            'level': 1
        },
        {
            'username': 'sofia.dev',
            'email': 'sofia@estudiante.edu.ar',
            'first_name': 'Sofia',
            'last_name': 'Lopez',
            'bio': 'Full-stack developer en formacion. React, Node.js y bases de datos.',
            'student_id': 'EST004',
            'career': 'TSDS',
            'current_semester': 4,
            'total_points': 1200,
            'level': 4
        }
    ]
    
    usuarios_creados = {}
    for usuario_data in usuarios_data:
        career_key = usuario_data.pop('career')
        carrera = carreras.get(career_key)
        
        usuario, created = User.objects.get_or_create(
            username=usuario_data['username'],
            defaults={
                **usuario_data,
                'career': carrera,
                'enrollment_year': 2023
            }
        )
        
        if created:
            usuario.set_password('password123')
            usuario.save()
            print(f"Usuario creado: {usuario.username}")
        else:
            print(f"Usuario ya existe: {usuario.username}")
        
        usuarios_creados[usuario.username] = usuario
    
    return usuarios_creados


def crear_logros():
    print("Creando logros...")
    
    logros_data = [
        {
            'name': 'Primer Post',
            'description': 'Publicaste tu primera publicacion en la red social',
            'achievement_type': 'social',
            'level': 'bronze',
            'points': 10,
            'icon': 'fa-edit',
            'condition_description': 'Crear tu primera publicacion'
        },
        {
            'name': 'Mentor Activo',
            'description': 'Ayudaste a 10 estudiantes con sus consultas',
            'achievement_type': 'social',
            'level': 'gold',
            'points': 100,
            'icon': 'fa-chalkboard-teacher',
            'condition_description': 'Responder 10 consultas de estudiantes'
        },
        {
            'name': 'Estudiante Destacado',
            'description': 'Alcanzaste 1000 puntos de experiencia',
            'achievement_type': 'academic',
            'level': 'silver',
            'points': 50,
            'icon': 'fa-star',
            'condition_description': 'Acumular 1000 puntos de experiencia'
        },
        {
            'name': 'Compartir es Cuidar',
            'description': 'Compartiste 5 apuntes que fueron favoritos de otros',
            'achievement_type': 'academic',
            'level': 'silver',
            'points': 75,
            'icon': 'fa-share-alt',
            'condition_description': 'Compartir 5 apuntes populares'
        },
        {
            'name': 'Programador Senior',
            'description': 'Completaste todas las materias de programacion',
            'achievement_type': 'completion',
            'level': 'platinum',
            'points': 200,
            'icon': 'fa-code',
            'condition_description': 'Aprobar todas las materias de programacion'
        }
    ]
    
    logros_creados = {}
    for logro_data in logros_data:
        logro, created = Achievement.objects.get_or_create(
            name=logro_data['name'],
            defaults=logro_data
        )
        logros_creados[logro_data['name']] = logro
        
        if created:
            print(f"Logro creado: {logro.name}")
        else:
            print(f"Logro ya existe: {logro.name}")
    
    return logros_creados


def crear_contenido_inicial(usuarios, materias):
    print("Creando contenido inicial...")
    
    posts_data = [
        {
            'author': 'prof.garcia',
            'content': 'Bienvenidos al nuevo sistema de red social institucional! Aqui podran compartir conocimientos, hacer consultas y colaborar en sus proyectos.',
            'post_type': 'announcement',
            'is_pinned': True
        },
        {
            'author': 'est.rodriguez',
            'content': 'Alguien tiene experiencia con React Native? Estoy empezando con desarrollo mobile y me cuesta entender los componentes.',
            'post_type': 'question',
            'subject': '2.1.1'
        },
        {
            'author': 'sofia.dev',
            'content': 'Comparti mi proyecto final de desarrollo web. Es un e-commerce completo con Django y React. Link en mi perfil!',
            'post_type': 'text',
            'tags': 'django,react,ecommerce,proyecto'
        }
    ]
    
    posts_creados = []
    for post_data in posts_data:
        author_username = post_data.pop('author')
        subject_code = post_data.pop('subject', None)
        
        author = usuarios.get(author_username)
        subject = materias.get(subject_code) if subject_code else None
        
        if author:
            post = Post.objects.create(
                author=author,
                subject=subject,
                **post_data
            )
            posts_creados.append(post)
            print(f"Post creado por {author.username}")
    
    if posts_creados:
        Comment.objects.create(
            author=usuarios['ana.sistemas'],
            post=posts_creados[1],
            content='Yo estoy aprendiendo React Native tambien! Te recomiendo el curso de la documentacion oficial.'
        )
        print("Comentarios creados")
    
    if '1.1.1' in materias:
        Note.objects.create(
            title='Algoritmos de Ordenamiento - Resumen',
            content='Resumen completo de los principales algoritmos de ordenamiento: Bubble Sort, Quick Sort, Merge Sort...',
            author=usuarios['sofia.dev'],
            subject=materias['1.1.1'],
            note_type='summary',
            tags='algoritmos,ordenamiento,programacion'
        )
        print("Notas creadas")


def main():
    print("Iniciando creacion de datos completos...")
    print("=" * 60)
    
    carreras = crear_carreras()
    print()
    
    materias = crear_materias(carreras)
    print()
    
    usuarios = crear_usuarios_avanzados(carreras)
    print()
    
    logros = crear_logros()
    print()
    
    crear_contenido_inicial(usuarios, materias)
    print()
    
    print("=" * 60)
    print("RESUMEN FINAL:")
    print(f"Carreras: {Career.objects.count()}")
    print(f"Materias: {Subject.objects.count()}")
    print(f"Usuarios: {User.objects.count()}")
    print(f"Logros: {Achievement.objects.count()}")
    print(f"Posts: {Post.objects.count()}")
    print(f"Comentarios: {Comment.objects.count()}")
    print(f"Notas: {Note.objects.count()}")
    print()
    
    print("Datos completos creados exitosamente!")
    print("Accede al sistema en: http://127.0.0.1:8000/")
    print("Django Admin en: http://127.0.0.1:8000/admin/")
    print("Credenciales admin: admin / password123")


if __name__ == '__main__':
    main()