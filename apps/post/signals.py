"""
Signals para gamificación automática.
Se ejecutan automáticamente cuando se crean modelos.

Para usar:
1. Crear este archivo en apps/post/signals.py
2. Importar en apps/post/apps.py en el método ready()
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.post.models import Post
from apps.comment.models import Comment
from apps.like.models import Like
from apps.main.services.gamification_service import GamificationService


@receiver(post_save, sender=Post)
def award_points_for_post(sender, instance, created, **kwargs):
    """Otorga puntos cuando se crea un post"""
    if created and instance.author:
        result = GamificationService.award_points(
            user=instance.author,
            source='post',
            description=f'Post creado: "{instance.content[:50]}..."'
        )
        
        # Verificar logros desbloqueados
        GamificationService.check_achievements(instance.author)


@receiver(post_save, sender=Comment)
def award_points_for_comment(sender, instance, created, **kwargs):
    """Otorga puntos cuando se crea un comentario"""
    if created and instance.author:
        result = GamificationService.award_points(
            user=instance.author,
            source='comment',
            description=f'Comentario creado en post de {instance.post.author.username}'
        )
        
        # Verificar logros desbloqueados
        GamificationService.check_achievements(instance.author)


@receiver(post_save, sender=Like)
def award_points_for_like(sender, instance, created, **kwargs):
    """Otorga puntos al autor cuando recibe un like"""
    if created:
        # Obtener el objeto original (post, comment, etc)
        content_object = instance.content_object
        
        if content_object and hasattr(content_object, 'author'):
            result = GamificationService.award_points(
                user=content_object.author,
                source='like_received',
                description=f'{instance.user.username} te dio like'
            )
            
            # Verificar logros desbloqueados
            GamificationService.check_achievements(content_object.author)

"""
INTEGRACIÓN EN apps/post/apps.py:

from django.apps import AppConfig


class PostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.post'
    
    def ready(self):
        import apps.post.signals  # Importar signals

INTEGRACIÓN EN apps/comment/apps.py:

from django.apps import AppConfig


class CommentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.comment'
    
    def ready(self):
        import apps.comment.signals  # Importar signals

INTEGRACIÓN EN apps/like/apps.py:

from django.apps import AppConfig


class LikeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.like'
    
    def ready(self):
        import apps.like.signals  # Importar signals
"""
