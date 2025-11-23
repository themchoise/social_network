from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse
from apps.user.models import User
import logging

logger = logging.getLogger(__name__)


def custom_login_required(view_func):
    """
    Decorador personalizado que redirige a login personalizado en lugar de Django admin
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vista de login personalizado"""
    if request.user.is_authenticated:
        return redirect('post:timeline')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, 'Por favor ingresa usuario y contraseña')
            return render(request, 'auth/login.html')
        
        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.get_full_name_or_username()}!')
            
            # Redirigir a next o al timeline
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('post:timeline')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return render(request, 'auth/login.html', {
                'username': username
            })
    
    # GET request: limpiar mensajes previos
    storage = messages.get_messages(request)
    storage.used = True
    
    return render(request, 'auth/login.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Vista de registro personalizado"""
    if request.user.is_authenticated:
        return redirect('post:timeline')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        # Validaciones
        errors = []
        
        if not username:
            errors.append('El usuario es requerido')
        elif len(username) < 3:
            errors.append('El usuario debe tener al menos 3 caracteres')
        elif User.objects.filter(username=username).exists():
            errors.append('Este usuario ya existe')
        
        if not email:
            errors.append('El email es requerido')
        elif User.objects.filter(email=email).exists():
            errors.append('Este email ya está registrado')
        
        if not password:
            errors.append('La contraseña es requerida')
        elif len(password) < 6:
            errors.append('La contraseña debe tener al menos 6 caracteres')
        
        if password != password_confirm:
            errors.append('Las contraseñas no coinciden')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'auth/register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            })
        
        # Crear usuario
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            
            # Autenticar y loguear
            user = authenticate(request, username=username, password=password)
            login(request, user)
            
            messages.success(request, f'Bienvenido {user.get_full_name_or_username()}!')
            return redirect('post:timeline')
        
        except Exception as e:
            # Log del error real (solo en servidor)
            logger.error(f'Error en registro de usuario {username}: {str(e)}', exc_info=True)
            # Mostrar mensaje genérico al usuario
            messages.error(request, 'Ocurrió un error durante el registro. Por favor intenta de nuevo.')
            return render(request, 'auth/register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            })
    
    # GET request: limpiar mensajes previos
    storage = messages.get_messages(request)
    storage.used = True
    
    return render(request, 'auth/register.html')


@login_required(login_url='user:login')
def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('user:login')


@login_required(login_url='user:login')
def profile_view(request, username=None):
    """Vista de perfil de usuario"""
    if username is None:
        # Ver perfil propio
        user = request.user
    else:
        # Ver perfil de otro usuario
        user = User.objects.get(username=username)
    
    # Obtener posts del usuario
    posts = user.posts.select_related('author').filter(
        is_hidden=False
    ).order_by('-created_at')[:20]
    
    contexto = {
        'titulo': f'Perfil - {user.get_full_name_or_username()}',
        'profile_user': user,
        'posts': posts,
        'is_own_profile': request.user == user,
    }
    
    return render(request, 'auth/profile.html', contexto)
