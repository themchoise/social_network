from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('main/', views.InicioRedirectView.as_view(), name='inicio'),
    path('usuarios/', views.UsuariosListView.as_view(), name='lista_usuarios'),
    path('carreras/', views.CarrerasListView.as_view(), name='lista_carreras'),
    path('api/usuarios/', views.ApiUsuariosView.as_view(), name='api_usuarios'),
    path('help/', views.HelpView.as_view(), name='help'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),

    # Gamificación
    path('api/award-points/', views.AwardPointsView.as_view(), name='award_points'),
    path('api/user-stats/', views.UserStatsView.as_view(), name='get_user_stats'),
    path('api/user-achievements/', views.UserAchievementsView.as_view(), name='get_user_achievements'),
    path('api/points-history/', views.PointsHistoryView.as_view(), name='get_points_history'),
    path('api/check-achievements/', views.CheckAchievementsView.as_view(), name='check_achievements'),
    path('api/leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
]
