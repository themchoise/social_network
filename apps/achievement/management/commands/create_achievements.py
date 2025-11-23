"""
Comando para crear logros de ejemplo en la base de datos.

Uso: python manage.py create_achievements

Los logros creados pueden modificarse desde el admin de Django.
"""

from django.core.management.base import BaseCommand
from apps.achievement.models import Achievement


class Command(BaseCommand):
    help = 'Crea logros de ejemplo para el sistema de gamificación'

    def handle(self, *args, **options):
        achievements_data = [
            # Logros Académicos
            {
                'name': 'Primer Paso',
                'description': 'Crea tu primer post en la red social',
                'achievement_type': 'academic',
                'level': 'bronze',
                'points': 10,
                'icon': '👣',
                'condition_description': 'first post',
            },
            {
                'name': 'Participante Activo',
                'description': 'Crea 10 posts en la red social',
                'achievement_type': 'academic',
                'level': 'silver',
                'points': 25,
                'icon': '✍️',
                'condition_description': 'posts 10',
            },
            {
                'name': 'Creador Prolífico',
                'description': 'Crea 50 posts en la red social',
                'achievement_type': 'academic',
                'level': 'gold',
                'points': 50,
                'icon': '📚',
                'condition_description': 'posts 50',
            },
            {
                'name': 'Maestro de Contenido',
                'description': 'Crea 100 posts en la red social',
                'achievement_type': 'academic',
                'level': 'platinum',
                'points': 100,
                'icon': '📖',
                'condition_description': 'posts 100',
            },
            
            # Logros Sociales
            {
                'name': 'Voz en la Comunidad',
                'description': 'Crea tu primer comentario',
                'achievement_type': 'social',
                'level': 'bronze',
                'points': 5,
                'icon': '💬',
                'condition_description': 'first comment',
            },
            {
                'name': 'Conversador Ávido',
                'description': 'Crea 25 comentarios en la red social',
                'achievement_type': 'social',
                'level': 'silver',
                'points': 30,
                'icon': '🗣️',
                'condition_description': 'comments 25',
            },
            {
                'name': 'Experto en Diálogo',
                'description': 'Crea 100 comentarios en la red social',
                'achievement_type': 'social',
                'level': 'gold',
                'points': 75,
                'icon': '🎤',
                'condition_description': 'comments 100',
            },
            {
                'name': 'Embajador del Conocimiento',
                'description': 'Crea 250 comentarios en la red social',
                'achievement_type': 'social',
                'level': 'platinum',
                'points': 150,
                'icon': '🌟',
                'condition_description': 'comments 250',
            },
            
            # Logros de Completación
            {
                'name': 'Novato de la Comunidad',
                'description': 'Alcanza 100 puntos totales',
                'achievement_type': 'completion',
                'level': 'bronze',
                'points': 15,
                'icon': '🎯',
                'condition_description': 'total points 100',
            },
            {
                'name': 'Colaborador Confiable',
                'description': 'Alcanza 500 puntos totales',
                'achievement_type': 'completion',
                'level': 'silver',
                'points': 40,
                'icon': '🏅',
                'condition_description': 'total points 500',
            },
            {
                'name': 'Leyenda de la Red',
                'description': 'Alcanza 2000 puntos totales',
                'achievement_type': 'completion',
                'level': 'gold',
                'points': 80,
                'icon': '👑',
                'condition_description': 'total points 2000',
            },
            {
                'name': 'Deidad de la Comunidad',
                'description': 'Alcanza 5000 puntos totales',
                'achievement_type': 'completion',
                'level': 'platinum',
                'points': 200,
                'icon': '⚡',
                'condition_description': 'total points 5000',
            },
            
            # Logros de Hito
            {
                'name': 'Nivel 2',
                'description': 'Alcanza el nivel 2',
                'achievement_type': 'milestone',
                'level': 'bronze',
                'points': 20,
                'icon': '2️⃣',
                'condition_description': 'level 2',
            },
            {
                'name': 'Nivel 5',
                'description': 'Alcanza el nivel 5',
                'achievement_type': 'milestone',
                'level': 'silver',
                'points': 50,
                'icon': '5️⃣',
                'condition_description': 'level 5',
            },
            {
                'name': 'Nivel 10',
                'description': 'Alcanza el nivel 10',
                'achievement_type': 'milestone',
                'level': 'gold',
                'points': 100,
                'icon': '🔟',
                'condition_description': 'level 10',
            },
            {
                'name': 'Nivel Máximo',
                'description': 'Alcanza el nivel 20',
                'achievement_type': 'milestone',
                'level': 'platinum',
                'points': 250,
                'icon': '🚀',
                'condition_description': 'level 20',
            },
            
            # Logros Especiales
            {
                'name': 'Bienvenido a la Familia',
                'description': 'Únete a la red social y crea tu perfil',
                'achievement_type': 'special',
                'level': 'bronze',
                'points': 5,
                'icon': '👋',
                'condition_description': 'signup',
            },
            {
                'name': 'Día de Suerte',
                'description': 'Obtén tu primer like',
                'achievement_type': 'special',
                'level': 'bronze',
                'points': 10,
                'icon': '🍀',
                'condition_description': 'first like',
            },
            {
                'name': 'Estrella en Ascenso',
                'description': 'Recibe 50 likes en tus contenidos',
                'achievement_type': 'special',
                'level': 'silver',
                'points': 35,
                'icon': '⭐',
                'condition_description': 'likes 50',
            },
            {
                'name': 'Sensación de la Red',
                'description': 'Recibe 500 likes en tus contenidos',
                'achievement_type': 'special',
                'level': 'gold',
                'points': 90,
                'icon': '✨',
                'condition_description': 'likes 500',
            },
        ]

        created_count = 0
        for data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'achievement_type': data['achievement_type'],
                    'level': data['level'],
                    'points': data['points'],
                    'icon': data['icon'],
                    'condition_description': data['condition_description'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creado: {achievement.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'→ Ya existe: {achievement.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✨ Total de logros creados: {created_count}')
        )
