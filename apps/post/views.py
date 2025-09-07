from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def timeline(request):
    contexto = {
        'titulo': 'Timeline - Red Social',
        'mensaje': 'Completa los modelos para ver el timeline'
    }
    
    return render(request, 'post/timeline.html', contexto)

@login_required
def crear_post(request):
    return render(request, 'post/crear_post.html')

@login_required
def toggle_like(request, post_id):
    return render(request, 'post/timeline.html', {'mensaje': 'Funcionalidad en desarrollo'})
