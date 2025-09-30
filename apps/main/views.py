from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import django
from apps.user.models import User
from apps.career.models import Career

def inicio(request):
    return render(request, 'timeline.html')

def timeline(request):
    return render(request, 'timeline.html')

def help_view(request):
    """
    Vista de ayuda que muestra información útil para los usuarios
    """
    context = {
        'debug': settings.DEBUG,
        'django_version': django.get_version(),
    }
    return render(request, 'help.html', context)

def lista_usuarios(request):
    usuarios = User.objects.select_related('career').all()
    context = {
        'usuarios': usuarios,
    }
    return render(request, 'main/lista_usuarios.html', context)

def lista_carreras(request):
    carreras = Career.objects.prefetch_related('students').all()
    context = {
        'carreras': carreras,
    }
    return render(request, 'main/lista_carreras.html', context)

def api_usuarios(request):
    if request.method == 'GET':
        try:
            usuarios = User.objects.select_related('career').all()
            usuarios_data = []
            
            for usuario in usuarios:
                usuario_info = {
                    'id': usuario.id,
                    'username': usuario.username,
                    'email': usuario.email,
                    'career': usuario.career.name if usuario.career else None,
                    'bio': usuario.bio,
                    'total_points': usuario.total_points,
                    'level': usuario.level,
                    'created_at': usuario.created_at.isoformat()
                }
                
                usuarios_data.append(usuario_info)
            
            return JsonResponse({
                'usuarios': usuarios_data,
                'total': len(usuarios_data)
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

