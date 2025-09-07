from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('main/', views.inicio, name='inicio'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('carreras/', views.lista_carreras, name='lista_carreras'),
    path('api/usuarios/', views.api_usuarios, name='api_usuarios'),
]
