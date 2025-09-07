"""
URL configuration for socialnetwork_project project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.post.urls')),
    path('usuario/', include('apps.usuario.urls')),
]
