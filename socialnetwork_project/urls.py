from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.post.urls')),
    path('usuario/', include('apps.usuario.urls')),
    path('', include('apps.main.urls')),
]
