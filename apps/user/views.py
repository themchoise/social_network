from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic.edit import FormView, CreateView
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from apps.user.models import User
from apps.user.forms import LoginForm, RegisterForm
import logging

logger = logging.getLogger(__name__)


class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('post:timeline')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.cleaned_data.get('user')
        login(self.request, user)
        messages.success(self.request, f'Bienvenido {user.get_full_name_or_username()}!')
        next_url = self.request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return super().form_valid(form)


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('post:timeline')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            user = form.save()
            login(self.request, user)
            messages.success(self.request, f'Bienvenido {user.get_full_name_or_username()}!')
            return redirect(self.get_success_url())
        except Exception as e:
            logger.error(f'Error en registro de usuario: {e}', exc_info=True)
            messages.error(self.request, 'Ocurrió un error durante el registro. Por favor intenta de nuevo.')
            return super().form_invalid(form)


class LogoutView(LoginRequiredMixin, View):
    login_url = 'user:login'

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente')
        return redirect('user:login')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'auth/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    login_url = 'user:login'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        if not username:
            return self.request.user
        return User.objects.get(username=username)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.object
        posts = user.posts.select_related('author').filter(is_hidden=False).order_by('-created_at')[:20]
        ctx.update({
            'titulo': f'Perfil - {user.get_full_name_or_username()}',
            'posts': posts,
            'is_own_profile': self.request.user == user,
        })
        return ctx
