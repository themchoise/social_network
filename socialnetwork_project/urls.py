from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.post.urls')),
    path('user/', include('apps.user.urls')),
    path('', include('apps.main.urls')),
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configurar handlers de error personalizados
handler404 = 'socialnetwork_project.error_handlers.handler404'
handler500 = 'socialnetwork_project.error_handlers.handler500'
handler403 = 'socialnetwork_project.error_handlers.handler403'
