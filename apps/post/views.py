from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.post.models import Post
from apps.post.forms import PostForm
from apps.main.services.gamification_service import GamificationService
import logging

logger = logging.getLogger(__name__)


def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def get_comments_data(post, current_user):
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
            'is_author': comment.author == current_user
        })
    return comentarios_data


class TimelineView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/timeline.html'
    context_object_name = 'posts'
    login_url = 'user:login'

    def get_queryset(self):
        return Post.objects.select_related('author').filter(is_hidden=False).order_by('-created_at')[:50]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Timeline - Red Social'
        ctx['is_authenticated'] = self.request.user.is_authenticated
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/crear_post.html'
    login_url = 'user:login'
    success_url = reverse_lazy('post:timeline')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = form.cleaned_data.get('post_type') or 'text'
        form.instance.privacy_level = form.cleaned_data.get('privacy_level') or 'public'
        p = form.save()

        try:
            gamification_result = GamificationService.award_points(
                user=self.request.user,
                source='post',
                description=f'Post creado: "{p.content[:50]}..."'
            )
            achievements_result = GamificationService.check_achievements(self.request.user)
        except Exception:
            gamification_result = {}
            achievements_result = []

        if is_ajax(self.request):
            return JsonResponse({
                'success': True,
                'post': {
                    'id': p.id,
                    'content': p.content,
                    'author': p.author.username,
                    'created_at': p.created_at.isoformat(),
                    'post_type': p.post_type,
                },
                'gamification': {**gamification_result, 'achievements_unlocked': achievements_result}
            })
        messages.success(self.request, 'Post creado exitosamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        if is_ajax(self.request):
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        messages.error(self.request, 'Revisá los errores del formulario')
        return super().form_invalid(form)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post/detalle_post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    login_url = 'user:login'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_view(request.user):
            return render(request, 'errors/403.html', status=403)

        self.object.increment_views()
        comentarios = self.object.comments.select_related('author').order_by('-created_at')
        contexto = {
            'post': self.object,
            'comentarios': comentarios,
        }
        return render(request, self.template_name, contexto)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            content = request.POST.get('content', '').strip()
            if not content:
                if is_ajax(request):
                    return JsonResponse({'success': False, 'error': 'El comentario no puede estar vacío'}, status=400)

            from apps.comment.models import Comment

            comment = Comment.objects.create(
                author=request.user,
                post=self.object,
                content=content
            )

            try:
                gamification_result = GamificationService.award_points(
                    user=request.user,
                    source='comment',
                    description=f'Comentario creado en post de {self.object.author.username}'
                )
            except Exception:
                gamification_result = {}

            if is_ajax(request):
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

            return redirect('post:detalle', post_id=self.object.id)

        except Exception as e:
            if is_ajax(request):
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
            return redirect('post:detalle', post_id=self.object.id)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/editar_post.html'
    pk_url_kwarg = 'post_id'
    login_url = 'user:login'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def form_valid(self, form):
        p = form.save()
        if is_ajax(self.request):
            return JsonResponse({'success': True, 'message': 'Post actualizado exitosamente'})
        messages.success(self.request, 'Cambios guardados')
        return redirect('post:detalle', post_id=p.id)

    def form_invalid(self, form):
        if is_ajax(self.request):
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        messages.error(self.request, 'Errores al guardar, revisá el formulario')
        return super().form_invalid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post/confirmar_eliminar.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('post:timeline')
    login_url = 'user:login'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            if is_ajax(request):
                return JsonResponse({'success': True, 'message': 'Post eliminado exitosamente'})
            return redirect(self.success_url)
        except Exception as e:
            if is_ajax(request):
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
            return render(request, self.template_name, {'post': self.object, 'error': str(e)})




class GetCommentsView(LoginRequiredMixin, View):
    login_url = 'user:login'

    def get(self, request, post_id, *args, **kwargs):
        try:
            post = get_object_or_404(Post, id=post_id)
            if not post.can_view(request.user):
                return JsonResponse({'success': False, 'error': 'No tienes permiso para ver este post'}, status=403)
            comentarios_data = get_comments_data(post, request.user)
            return JsonResponse({'success': True, 'count': len(comentarios_data), 'comments': comentarios_data})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class ToggleLikeView(LoginRequiredMixin, View):
    login_url = 'user:login'

    def post(self, request, post_id, *args, **kwargs):
        try:
            post = get_object_or_404(Post, id=post_id)

            if post.privacy_level == 'private' and post.author != request.user:
                return JsonResponse({
                    'success': False,
                    'error': 'No tienes permiso para dar like a este post'
                }, status=403)

            from apps.like.models import Like
            from django.contrib.contenttypes.models import ContentType

            try:
                content_type = ContentType.objects.get_for_model(Post)
                if content_type is None:
                    raise ValueError("ContentType para Post no pudo ser determinado")

                like, created = Like.objects.get_or_create(
                    user=request.user,
                    content_type=content_type,
                    object_id=post.id
                )
            except ContentType.DoesNotExist as e:
                logger.error(f"ContentType para Post no existe: {e}", exc_info=True)
                return JsonResponse({
                    'success': False,
                    'error': 'Error del sistema: tipo de contenido no encontrado'
                }, status=500)
            except ValueError as e:
                logger.error(f"No se pudo obtener ContentType: {e}", exc_info=True)
                return JsonResponse({
                    'success': False,
                    'error': 'Error del sistema: no se pudo obtener el tipo de contenido'
                }, status=500)
            except Exception as e:
                logger.error(f"Error al crear/obtener like: {e}", exc_info=True)
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
                logger.error(f"Error contando likes: {e}", exc_info=True)
                like_count = 0

            if created:
                try:
                    gamification_result = GamificationService.award_points(
                        user=post.author,
                        source='like_received',
                        description=f'{request.user.username} te dio like en un post'
                    )

                    achievements_result = GamificationService.check_achievements(post.author)
                except Exception as e:
                    logger.error(f"Error en gamification: {e}", exc_info=True)
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
                try:
                    like.delete()
                except Exception as e:
                    logger.error(f"Error eliminando like: {e}", exc_info=True)
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
            logger.error(f"Error en toggle_like: {str(e)}", exc_info=True)
            return JsonResponse({
                'success': False,
                'error': f'Error al procesar like: {str(e)}'
            }, status=500)



