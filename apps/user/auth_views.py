from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from apps.user.models import User

@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vista de login personalizado"""
    if request.user.is_authenticated:
        return redirect('post:timeline')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('post:timeline')
        else:
            return render(request, 'auth/login.html', {
                'error': 'Usuario o contraseña incorrectos',
                'username': username
            })
    
    return render(request, 'auth/login.html')

@require_http_methods(["GET", "POST"])
def register_view(request):
    """Vista de registro personalizado"""
    if request.user.is_authenticated:
        return redirect('post:timeline')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        errors = {}
        
        # Validar campos
        if not username:
            errors['username'] = 'El usuario es requerido'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'El usuario ya existe'
        
        if not email:
            errors['email'] = 'El email es requerido'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'El email ya está registrado'
        
        if not password:
            errors['password'] = 'La contraseña es requerida'
        elif len(password) < 6:
            errors['password'] = 'La contraseña debe tener al menos 6 caracteres'
        
        if password != password_confirm:
            errors['password_confirm'] = 'Las contraseñas no coinciden'
        
        if errors:
            return render(request, 'auth/register.html', {
                'errors': errors,
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            })
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        
        login(request, user)
        return redirect('post:timeline')
    
    return render(request, 'auth/register.html')

@login_required
def logout_view(request):
    """Vista de logout"""
    logout(request)
    return redirect('user:login')
