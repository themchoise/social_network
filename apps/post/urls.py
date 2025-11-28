from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.TimelineView.as_view(), name='timeline'),
    path('crear/', views.PostCreateView.as_view(), name='crear'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='detalle'),
    path('<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('<int:post_id>/comments/', views.get_comments, name='get_comments'),
    path('<int:post_id>/editar/', views.PostUpdateView.as_view(), name='editar'),
    path('<int:post_id>/eliminar/', views.PostDeleteView.as_view(), name='eliminar'),
]
