from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from apps.usuario.models import PerfilUsuario, Carrera

def inicio(request):
    return render(request, 'main/inicio.html')

def lista_usuarios(request):
    usuarios = User.objects.select_related('perfil', 'perfil__carrera').all()
    context = {
        'usuarios': usuarios,
    }
    return render(request, 'main/lista_usuarios.html', context)

def lista_carreras(request):
    carreras = Carrera.objects.prefetch_related('estudiantes__usuario').all()
    context = {
        'carreras': carreras,
    }
    return render(request, 'main/lista_carreras.html', context)

def api_usuarios(request):
    if request.method == 'GET':
        try:
            usuarios = User.objects.select_related('perfil').all()
            usuarios_data = []
            
            for usuario in usuarios:
                usuario_info = {
                    'id': usuario.id,
                    'username': usuario.username,
                    'email': usuario.email,
                    'perfil': None
                }
                
                if hasattr(usuario, 'perfil'):
                    usuario_info['perfil'] = {
                        'nombre': usuario.perfil.nombre,
                        'carrera': usuario.perfil.carrera.nombre if usuario.perfil.carrera else None,
                        'creation_date': usuario.perfil.creation_date.isoformat()
                    }
                
                usuarios_data.append(usuario_info)
            
            return JsonResponse({
                'usuarios': usuarios_data,
                'total': len(usuarios_data)
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

