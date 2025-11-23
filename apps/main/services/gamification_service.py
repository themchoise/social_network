"""
Servicio de gamificación para la red social.
Maneja la lógica de otorgar puntos por diferentes acciones.
"""

from django.db import transaction
from apps.user.models import User, UserPointsHistory
from apps.achievement.models import UserAchievement, Achievement


# Configuración de puntos por acción
POINTS_CONFIG = {
    'post': 10,
    'comment': 5,
    'like_received': 2,
    'note_shared': 8,
    'achievement_unlocked': 0,  # Los puntos vienen del achievement
    'login_streak': 3,
    'help_others': 15,
    'admin_bonus': 0,
}


class GamificationService:
    """Servicio para gestionar la gamificación de la red social."""
    
    @staticmethod
    @transaction.atomic
    def award_points(user: User, source: str, points: int = None, description: str = None) -> dict:
        """
        Otorga puntos a un usuario por una acción.
        
        Args:
            user: Usuario que recibe los puntos
            source: Tipo de acción (post, comment, etc)
            points: Cantidad de puntos (si no se proporciona, usa la configuración)
            description: Descripción personalizada del evento
            
        Returns:
            dict con información de los puntos otorgados y cambios de nivel
        """
        if not user:
            return {'success': False, 'error': 'Usuario no válido'}
        
        if source not in POINTS_CONFIG:
            return {'success': False, 'error': f'Fuente de puntos desconocida: {source}'}
        
        # Usar puntos proporcionados o los de configuración
        if points is None:
            points = POINTS_CONFIG[source]
        
        if points <= 0:
            return {'success': False, 'error': 'Los puntos deben ser mayores a 0'}
        
        # Guardar información previa de nivel
        old_level = user.level
        old_experience = user.experience_points
        
        # Crear registro en historial
        points_history = UserPointsHistory.objects.create(
            user=user,
            points=points,
            source=source,
            description=description or f'Puntos por {source}'
        )
        
        # Actualizar puntos del usuario
        user.add_points(points)
        
        # Verificar si hubo cambio de nivel
        level_up = user.level > old_level
        
        return {
            'success': True,
            'points': points,
            'total_points': user.total_points,
            'level': user.level,
            'level_up': level_up,
            'level_change': user.level - old_level if level_up else 0,
            'experience_points': user.experience_points,
            'points_history_id': points_history.id,
        }
    
    @staticmethod
    def award_achievement(user: User, achievement: Achievement) -> dict:
        """
        Otorga un logro a un usuario.
        
        Args:
            user: Usuario que recibe el logro
            achievement: Logro a otorgar
            
        Returns:
            dict con información del logro y puntos obtenidos
        """
        if not user or not achievement:
            return {'success': False, 'error': 'Usuario o logro no válido'}
        
        # Verificar si el usuario ya tiene este logro
        existing = UserAchievement.objects.filter(
            user=user,
            achievement=achievement
        ).exists()
        
        if existing:
            return {'success': False, 'error': 'Este usuario ya tiene este logro'}
        
        # Crear el logro del usuario
        user_achievement = UserAchievement.objects.create(
            user=user,
            achievement=achievement
        )
        
        # Otorgar puntos del logro
        result = GamificationService.award_points(
            user=user,
            source='achievement',
            points=achievement.points,
            description=f'Logro desbloqueado: {achievement.name}'
        )
        
        return {
            'success': True,
            'achievement': {
                'id': achievement.id,
                'name': achievement.name,
                'description': achievement.description,
                'level': achievement.level,
                'icon': achievement.icon,
                'points': achievement.points,
            },
            'points_awarded': achievement.points,
            **result
        }
    
    @staticmethod
    def check_achievements(user: User) -> list:
        """
        Verifica y desbloquea logros para un usuario basado en sus estadísticas.
        
        Args:
            user: Usuario a verificar
            
        Returns:
            list de logros desbloqueados
        """
        unlocked_achievements = []
        
        # Obtener todos los logros activos que el usuario no tiene
        available_achievements = Achievement.objects.filter(
            is_active=True
        ).exclude(
            user_achievements__user=user
        )
        
        for achievement in available_achievements:
            if GamificationService._check_achievement_condition(user, achievement):
                result = GamificationService.award_achievement(user, achievement)
                if result['success']:
                    unlocked_achievements.append(result)
        
        return unlocked_achievements
    
    @staticmethod
    def _check_achievement_condition(user: User, achievement: Achievement) -> bool:
        """
        Verifica si un usuario cumple las condiciones para desbloquear un logro.
        
        Args:
            user: Usuario a verificar
            achievement: Logro a verificar
            
        Returns:
            True si el usuario cumple las condiciones
        """
        # Esta es una lógica base que puede expandirse
        # basada en el nombre o descripción del logro
        
        condition = achievement.condition_description.lower()
        
        # Verificar condiciones comunes
        if 'first post' in condition:
            return user.posts.count() >= 1
        
        if 'first comment' in condition:
            from apps.comment.models import Comment
            return Comment.objects.filter(author=user).count() >= 1
        
        if 'total points' in condition:
            # Extraer número de la condición
            import re
            match = re.search(r'(\d+)', condition)
            if match:
                required_points = int(match.group(1))
                return user.total_points >= required_points
        
        if 'posts' in condition:
            import re
            match = re.search(r'(\d+)', condition)
            if match:
                required_posts = int(match.group(1))
                return user.posts.count() >= required_posts
        
        if 'comments' in condition:
            import re
            from apps.comment.models import Comment
            match = re.search(r'(\d+)', condition)
            if match:
                required_comments = int(match.group(1))
                return Comment.objects.filter(author=user).count() >= required_comments
        
        if 'level' in condition:
            import re
            match = re.search(r'(\d+)', condition)
            if match:
                required_level = int(match.group(1))
                return user.level >= required_level
        
        return False
    
    @staticmethod
    def get_user_stats(user: User) -> dict:
        """
        Obtiene estadísticas de gamificación del usuario.
        
        Args:
            user: Usuario a consultar
            
        Returns:
            dict con estadísticas
        """
        from apps.comment.models import Comment
        from apps.post.models import Post
        
        total_posts = Post.objects.filter(author=user).count()
        total_comments = Comment.objects.filter(author=user).count()
        total_achievements = user.user_achievements.count()
        
        # Puntos por fuente
        points_by_source = {}
        history = UserPointsHistory.objects.filter(user=user)
        for source in ['post', 'comment', 'like_received', 'note_shared', 'achievement']:
            points_by_source[source] = history.filter(source=source).aggregate(
                total=__import__('django.db.models', fromlist=['Sum']).Sum('points')
            )['total'] or 0
        
        return {
            'user_id': user.id,
            'username': user.username,
            'level': user.level,
            'total_points': user.total_points,
            'experience_points': user.experience_points,
            'total_posts': total_posts,
            'total_comments': total_comments,
            'total_achievements': total_achievements,
            'points_by_source': points_by_source,
            'points_to_next_level': ((user.level + 1) * 1000) - user.experience_points,
        }
