from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.timeline, name='timeline'),
    path('crear/', views.crear_post, name='crear'),
    path('<int:post_id>/', views.detalle_post, name='detalle'),
    path('<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('<int:post_id>/comments/', views.get_comments, name='get_comments'),
    path('<int:post_id>/editar/', views.editar_post, name='editar'),
    path('<int:post_id>/eliminar/', views.eliminar_post, name='eliminar'),
]
