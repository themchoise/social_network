from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.post.models import Post
from apps.main.services.gamification_service import GamificationService
from apps.user.views import custom_login_required
import json


@custom_login_required
@require_http_methods(["GET"])
def get_comments(request, post_id):
    """Obtener comentarios de un post (AJAX)"""
    try:
        post = get_object_or_404(Post, id=post_id)
        
        # Verificar permisos de visualización
        if not post.can_view(request.user):
            return JsonResponse({
                'success': False,
                'error': 'No tienes permiso para ver este post'
            }, status=403)
        
        # Obtener comentarios
        comentarios = post.comments.select_related('author').order_by('-created_at')
        
        comentarios_data = []
        for comment in comentarios:
            comentarios_data.append({
                'id': comment.id,
                'author': comment.author.get_full_name_or_username(),
                'author_initial': comment.author.get_full_name_or_username()[0].upper(),
                'content': comment.content,
                'created_at': comment.created_at.isoformat(),
                'created_at_display': f"{comment.created_at.strftime('%d/%m/%Y %H:%M')}",
                'has_image': bool(comment.image),
                'image_url': comment.image.url if comment.image else None,
                'is_author': comment.author == request.user
            })
        
        return JsonResponse({
            'success': True,
            'count': len(comentarios_data),
            'comments': comentarios_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@custom_login_required
def timeline(request):
    """Vista del timeline con todos los posts"""
    posts = Post.objects.select_related('author').filter(
        is_hidden=False
    ).order_by('-created_at')[:50]
    
    contexto = {
        'titulo': 'Timeline - Red Social',
        'posts': posts,
        'is_authenticated': request.user.is_authenticated,
    }
    
    return render(request, 'post/timeline.html', contexto)


@custom_login_required
@require_http_methods(["GET", "POST"])
def crear_post(request):
    """Crear un nuevo post"""
    if request.method == 'POST':
        try:
            content = request.POST.get('content', '').strip()
            post_type = request.POST.get('post_type', 'TEXT')
            privacy = request.POST.get('privacy', 'public')
            
            # Validar contenido
            if not content:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'El contenido del post no puede estar vacío'
                    }, status=400)
                return render(request, 'post/crear_post.html', {
                    'error': 'El contenido del post no puede estar vacío'
                })
            
            if len(content) > 5000:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'El contenido es muy largo (máximo 5000 caracteres)'
                    }, status=400)
                return render(request, 'post/crear_post.html', {
                    'error': 'El contenido es muy largo (máximo 5000 caracteres)'
                })
            
            # Crear el post
            post = Post.objects.create(
                author=request.user,
                content=content,
                post_type=post_type.lower(),
                privacy_level=privacy,
            )
            
            # 🎮 OTORGAR PUNTOS POR GAMIFICACIÓN
            gamification_result = GamificationService.award_points(
                user=request.user,
                source='post',
                description=f'Post creado: "{content[:50]}..."'
            )
            
            # 🏆 VERIFICAR LOGROS DESBLOQUEADOS
            achievements_result = GamificationService.check_achievements(request.user)
            
            # Respuesta diferenciada para AJAX o formulario HTML
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'post': {
                        'id': post.id,
                        'content': post.content,
                        'author': post.author.username,
                        'created_at': post.created_at.isoformat(),
                        'post_type': post.post_type,
                    },
                    'gamification': {
                        **gamification_result,
                        'achievements_unlocked': achievements_result
                    }
                })
            
            return redirect('post:timeline')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': f'Error al crear post: {str(e)}'
                }, status=500)
            return render(request, 'post/crear_post.html', {
                'error': f'Error al crear post: {str(e)}'
            })
    
    # GET: mostrar formulario
    return render(request, 'post/crear_post.html')


@custom_login_required
def detalle_post(request, post_id):
    """Ver detalles de un post y crear comentarios"""
    post = get_object_or_404(Post, id=post_id)
    
    # Verificar permisos de visualización
    if not post.can_view(request.user):
        return render(request, 'errors/403.html', status=403)
    
    # Incrementar vistas
    post.increment_views()
    
    # Si es POST, crear un comentario
    if request.method == 'POST':
        try:
            content = request.POST.get('content', '').strip()
            
            if not content:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'El comentario no puede estar vacío'
                    }, status=400)
            
            from apps.comment.models import Comment
            
            # Crear el comentario
            comment = Comment.objects.create(
                author=request.user,
                post=post,
                content=content
            )
            
            # Otorgar puntos por comentar
            gamification_result = GamificationService.award_points(
                user=request.user,
                source='comment',
                description=f'Comentario creado en post de {post.author.username}'
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'id': comment.id,
                        'author': comment.author.get_full_name_or_username(),
                        'content': comment.content,
                        'created_at': comment.created_at.isoformat(),
                    },
                    'gamification': gamification_result
                })
            
            return redirect('post:detalle', post_id=post.id)
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)
            return redirect('post:detalle', post_id=post.id)
    
    # Obtener comentarios
    comentarios = post.comments.select_related('author').order_by('-created_at')
    
    contexto = {
        'post': post,
        'comentarios': comentarios,
    }
    
    return render(request, 'post/detalle_post.html', contexto)


@custom_login_required
@require_http_methods(["POST"])
def toggle_like(request, post_id):
    """Dar/quitar like a un post (AJAX)"""
    try:
        post = get_object_or_404(Post, id=post_id)
        
        # Verificar permisos - simplificar para evitar errores
        if post.privacy_level == 'private' and post.author != request.user:
            return JsonResponse({
                'success': False,
                'error': 'No tienes permiso para dar like a este post'
            }, status=403)
        
        # Obtener o crear el like
        from apps.like.models import Like
        from django.contrib.contenttypes.models import ContentType
        import traceback
        
        try:
            # Obtener ContentType de forma segura usando get_for_model
            # que es más confiable que parámetros
            content_type = ContentType.objects.get_for_model(Post)
            
            if content_type is None:
                raise ValueError("ContentType para Post no pudo ser determinado")
            
            like, created = Like.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                object_id=post.id
            )
        except ContentType.DoesNotExist as e:
            print(f"[ERROR] ContentType para Post no existe: {e}")
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': 'Error del sistema: tipo de contenido no encontrado'
            }, status=500)
        except ValueError as e:
            print(f"[ERROR] No se pudo obtener ContentType: {e}")
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': 'Error del sistema: no se pudo obtener el tipo de contenido'
            }, status=500)
        except Exception as e:
            print(f"[ERROR] Error al crear/obtener like: {e}")
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': f'Error al procesar like: {str(e)}'
            }, status=500)
        
        # Contar likes de forma segura
        try:
            like_count = Like.objects.filter(
                content_type=content_type,
                object_id=post.id
            ).count()
        except Exception as e:
            print(f"[ERROR] Error contando likes: {e}")
            import traceback
            traceback.print_exc()
            like_count = 0
        
        if created:
            # Nuevo like: otorgar puntos al autor
            try:
                gamification_result = GamificationService.award_points(
                    user=post.author,
                    source='like_received',
                    description=f'{request.user.username} te dio like en un post'
                )
                
                # Verificar logros del autor
                achievements_result = GamificationService.check_achievements(post.author)
            except Exception as e:
                print(f"[ERROR] Error en gamification: {e}")
                import traceback
                traceback.print_exc()
                gamification_result = {'points': 0}
                achievements_result = []
            
            return JsonResponse({
                'success': True,
                'liked': True,
                'like_count': like_count,
                'author_gamification': {
                    **gamification_result,
                    'achievements_unlocked': achievements_result
                }
            })
        else:
            # Eliminar like
            try:
                like.delete()
            except Exception as e:
                print(f"[ERROR] Error eliminando like: {e}")
                import traceback
                traceback.print_exc()
                return JsonResponse({
                    'success': False,
                    'error': f'Error al eliminar like: {str(e)}'
                }, status=500)
            
            return JsonResponse({
                'success': True,
                'liked': False,
                'like_count': like_count
            })
            
    except Exception as e:
        print(f"[ERROR] Error en toggle_like: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'Error al procesar like: {str(e)}'
        }, status=500)


@custom_login_required
def eliminar_post(request, post_id):
    """Eliminar un post (solo el autor)"""
    post = get_object_or_404(Post, id=post_id)
    
    # Verificar que el usuario es el autor
    if post.author != request.user:
        return render(request, 'errors/403.html', status=403)
    
    if request.method == 'POST':
        try:
            post.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Post eliminado exitosamente'
                })
            
            return redirect('post:timeline')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)
            return render(request, 'post/confirmar_eliminar.html', {'post': post, 'error': str(e)})
    
    return render(request, 'post/confirmar_eliminar.html', {'post': post})


@custom_login_required
def editar_post(request, post_id):
    """Editar un post (solo el autor)"""
    post = get_object_or_404(Post, id=post_id)
    
    # Verificar que el usuario es el autor
    if post.author != request.user:
        return render(request, 'errors/403.html', status=403)
    
    if request.method == 'POST':
        try:
            content = request.POST.get('content', '').strip()
            
            if not content:
                return render(request, 'post/editar_post.html', {
                    'post': post,
                    'error': 'El contenido no puede estar vacío'
                })
            
            post.content = content
            post.post_type = request.POST.get('post_type', post.post_type)
            post.privacy_level = request.POST.get('privacy', post.privacy_level)
            post.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Post actualizado exitosamente'
                })
            
            return redirect('post:detalle', post_id=post.id)
            
        except Exception as e:
            return render(request, 'post/editar_post.html', {
                'post': post,
                'error': f'Error al editar: {str(e)}'
            })
    
    return render(request, 'post/editar_post.html', {'post': post})
