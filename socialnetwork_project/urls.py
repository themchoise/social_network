from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import JsonResponse

def redirect_to_timeline(request):
    return redirect('/post/', permanent=False)

def health_check(request):
    """Endpoint simple para healthcheck del contenedor"""
    return JsonResponse({'status': 'ok', 'message': 'App is healthy'}, status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('', redirect_to_timeline),
    path('post/', include('apps.post.urls')),
    path('user/', include('apps.user.urls')),
    path('', include('apps.main.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'socialnetwork_project.error_handlers.handler404'
handler500 = 'socialnetwork_project.error_handlers.handler500'
handler403 = 'socialnetwork_project.error_handlers.handler403'
