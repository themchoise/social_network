from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('main/', views.inicio, name='inicio'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('carreras/', views.lista_carreras, name='lista_carreras'),
    path('api/usuarios/', views.api_usuarios, name='api_usuarios'),
    path('help/', views.help_view, name='help'),
    
    # Gamificación
    path('api/award-points/', views.award_points, name='award_points'),
    path('api/user-stats/', views.get_user_stats, name='get_user_stats'),
    path('api/user-achievements/', views.get_user_achievements, name='get_user_achievements'),
    path('api/points-history/', views.get_points_history, name='get_points_history'),
    path('api/check-achievements/', views.check_achievements, name='check_achievements'),
    path('api/leaderboard/', views.leaderboard, name='leaderboard'),
]
