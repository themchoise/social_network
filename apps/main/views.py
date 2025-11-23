from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import django
import json
from apps.user.models import User
from apps.career.models import Career
from apps.achievement.models import Achievement
from apps.main.services.gamification_service import GamificationService

def inicio(request):
    return redirect('/post/')

def timeline(request):
    return redirect('/post/')

def help_view(request):
    """
    Vista de ayuda que muestra información útil para los usuarios
    """
    context = {
        'debug': settings.DEBUG,
        'django_version': django.get_version(),
    }
    return render(request, 'help.html', context)

def lista_usuarios(request):
    usuarios = User.objects.select_related('career').all()
    context = {
        'usuarios': usuarios,
    }
    return render(request, 'main/lista_usuarios.html', context)

def lista_carreras(request):
    carreras = Career.objects.prefetch_related('students').all()
    context = {
        'carreras': carreras,
    }
    return render(request, 'main/lista_carreras.html', context)

def api_usuarios(request):
    if request.method == 'GET':
        try:
            usuarios = User.objects.select_related('career').all()
            usuarios_data = []
            
            for usuario in usuarios:
                usuario_info = {
                    'id': usuario.id,
                    'username': usuario.username,
                    'email': usuario.email,
                    'career': usuario.career.name if usuario.career else None,
                    'bio': usuario.bio,
                    'total_points': usuario.total_points,
                    'level': usuario.level,
                    'created_at': usuario.created_at.isoformat()
                }
                
                usuarios_data.append(usuario_info)
            
            return JsonResponse({
                'usuarios': usuarios_data,
                'total': len(usuarios_data)
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# ===== GAMIFICACIÓN =====

@login_required
@require_http_methods(["POST"])
def award_points(request):
    """
    API endpoint para otorgar puntos a un usuario.
    Espera JSON con: source, points (opcional), description (opcional)
    """
    try:
        data = json.loads(request.body)
        source = data.get('source')
        points = data.get('points')
        description = data.get('description')
        
        if not source:
            return JsonResponse({
                'success': False,
                'error': 'Source es requerido'
            }, status=400)
        
        result = GamificationService.award_points(
            user=request.user,
            source=source,
            points=points,
            description=description
        )
        
        # Si hay cambio de nivel, verificar logros
        if result.get('success') and result.get('level_up'):
            achievements = GamificationService.check_achievements(request.user)
            result['achievements_unlocked'] = achievements
        
        return JsonResponse(result)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def get_user_stats(request):
    """
    Obtiene las estadísticas de gamificación del usuario actual.
    """
    try:
        stats = GamificationService.get_user_stats(request.user)
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


@login_required
def get_user_achievements(request):
    """
    Obtiene los logros del usuario actual.
    """
    try:
        achievements = request.user.user_achievements.select_related('achievement').all()
        achievements_data = []
        
        for ua in achievements:
            achievement = ua.achievement
            achievements_data.append({
                'id': achievement.id,
                'name': achievement.name,
                'description': achievement.description,
                'type': achievement.achievement_type,
                'level': achievement.level,
                'points': achievement.points,
                'icon': achievement.icon,
                'earned_at': ua.earned_at.isoformat(),
            })
        
        return JsonResponse({
            'achievements': achievements_data,
            'total': len(achievements_data)
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


@login_required
def get_points_history(request):
    """
    Obtiene el historial de puntos del usuario.
    """
    try:
        limit = int(request.GET.get('limit', 20))
        history = request.user.points_history.all().order_by('-created_at')[:limit]
        
        history_data = []
        for record in history:
            history_data.append({
                'id': record.id,
                'points': record.points,
                'source': record.source,
                'description': record.description,
                'created_at': record.created_at.isoformat(),
            })
        
        return JsonResponse({
            'history': history_data,
            'total': len(history_data)
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


def leaderboard(request):
    """
    Vista del ranking de usuarios por puntos.
    """
    try:
        limit = int(request.GET.get('limit', 50))
        users = User.objects.all().order_by('-total_points')[:limit]
        
        leaderboard_data = []
        for idx, user in enumerate(users, 1):
            leaderboard_data.append({
                'rank': idx,
                'id': user.id,
                'username': user.username,
                'total_points': user.total_points,
                'level': user.level,
                'experience_points': user.experience_points,
                'posts': user.posts.count(),
                'achievements': user.user_achievements.count(),
            })
        
        return JsonResponse({
            'leaderboard': leaderboard_data,
            'total': len(leaderboard_data)
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


@login_required
def check_achievements(request):
    """
    Verifica y desbloquea logros para el usuario actual.
    """
    try:
        achievements = GamificationService.check_achievements(request.user)
        return JsonResponse({
            'success': True,
            'achievements_unlocked': achievements,
            'total': len(achievements)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

