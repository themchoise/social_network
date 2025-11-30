from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import TemplateView, ListView, FormView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import django
import json
from apps.user.models import User
from apps.career.models import Career
from apps.achievement.models import Achievement
from apps.main.services.gamification_service import GamificationService
from apps.main.forms import FeedbackForm


class InicioRedirectView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/post/')


class TimelineRedirectView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/post/')


class HelpView(TemplateView):
    template_name = 'help.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['debug'] = settings.DEBUG
        ctx['django_version'] = django.get_version()
        return ctx


class FeedbackView(LoginRequiredMixin, FormView):
    login_url = 'user:login'
    template_name = 'main/feedback.html'
    form_class = FeedbackForm
    success_url = '/'

    def form_valid(self, form):
        # Aquí podríamos enviar email o guardar en DB
        messages.success(self.request, 'Gracias por tu feedback, ¡lo recibimos!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corregí los errores del formulario.')
        return super().form_invalid(form)


class UsuariosListView(ListView):
    model = User
    template_name = 'main/lista_usuarios.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return User.objects.select_related('career').all()


class CarrerasListView(ListView):
    model = Career
    template_name = 'main/lista_carreras.html'
    context_object_name = 'carreras'

    def get_queryset(self):
        return Career.objects.prefetch_related('students').all()


class ApiUsuariosView(View):
    def get(self, request, *args, **kwargs):
        try:
            usuarios = User.objects.select_related('career').all()
            usuarios_data = []
            for usuario in usuarios:
                usuarios_data.append({
                    'id': usuario.id,
                    'username': usuario.username,
                    'email': usuario.email,
                    'career': usuario.career.name if usuario.career else None,
                    'bio': usuario.bio,
                    'total_points': usuario.total_points,
                    'level': usuario.level,
                    'created_at': usuario.created_at.isoformat()
                })
            return JsonResponse({'usuarios': usuarios_data, 'total': len(usuarios_data)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# ===== GAMIFICACIÓN (vistas API basadas en clases) =====


class AwardPointsView(LoginRequiredMixin, View):
    login_url = 'user:login'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            source = data.get('source')
            points = data.get('points')
            description = data.get('description')

            if not source:
                return JsonResponse({'success': False, 'error': 'Source es requerido'}, status=400)

            result = GamificationService.award_points(user=request.user, source=source, points=points, description=description)
            if result.get('success') and result.get('level_up'):
                achievements = GamificationService.check_achievements(request.user)
                result['achievements_unlocked'] = achievements
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class UserStatsView(LoginRequiredMixin, View):
    login_url = 'user:login'

    def get(self, request, *args, **kwargs):
        try:
            stats = GamificationService.get_user_stats(request.user)
            return JsonResponse(stats)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class UserAchievementsView(LoginRequiredMixin, View):
    login_url = 'user:login'

    def get(self, request, *args, **kwargs):
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
            return JsonResponse({'achievements': achievements_data, 'total': len(achievements_data)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class PointsHistoryView(LoginRequiredMixin, View):
    login_url = 'user:login'

    def get(self, request, *args, **kwargs):
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
            return JsonResponse({'history': history_data, 'total': len(history_data)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class LeaderboardView(LoginRequiredMixin, View):
    login_url = 'user:login'

    def get(self, request, *args, **kwargs):
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
            return JsonResponse({'leaderboard': leaderboard_data, 'total': len(leaderboard_data)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class CheckAchievementsView(LoginRequiredMixin, View):
    login_url = 'user:login'

    def get(self, request, *args, **kwargs):
        try:
            achievements = GamificationService.check_achievements(request.user)
            return JsonResponse({'success': True, 'achievements_unlocked': achievements, 'total': len(achievements)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


