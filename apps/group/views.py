from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from apps.group.models import Group
from apps.group.forms import GroupForm


class GroupListView(LoginRequiredMixin, ListView):
	model = Group
	template_name = 'group/list.html'
	context_object_name = 'groups'
	login_url = 'user:login'

	def get_queryset(self):
		qs = Group.objects.select_related('creator', 'subject', 'career').filter(is_active=True)
		q = self.request.GET.get('q')
		if q:
			qs = qs.filter(name__icontains=q)
		return qs.order_by('-created_at')


class GroupDetailView(LoginRequiredMixin, DetailView):
	model = Group
	template_name = 'group/detail.html'
	context_object_name = 'group'
	login_url = 'user:login'


class GroupCreateView(LoginRequiredMixin, CreateView):
	model = Group
	form_class = GroupForm
	template_name = 'group/form.html'
	success_url = reverse_lazy('group:list')
	login_url = 'user:login'

	def form_valid(self, form):
		form.instance.creator = self.request.user
		messages.success(self.request, 'Grupo creado')
		return super().form_valid(form)

	def form_invalid(self, form):
		messages.error(self.request, 'Errores en el formulario')
		return super().form_invalid(form)


class GroupUpdateView(LoginRequiredMixin, UpdateView):
	model = Group
	form_class = GroupForm
	template_name = 'group/form.html'
	login_url = 'user:login'

	def dispatch(self, request, *args, **kwargs):
		group = self.get_object()
		if not group.is_admin(request.user):
			messages.error(request, 'No puedes editar este grupo')
			return reverse_lazy('group:list')
		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return self.object.get_absolute_url()

	def form_valid(self, form):
		messages.success(self.request, 'Grupo actualizado')
		return super().form_valid(form)


class GroupDeleteView(LoginRequiredMixin, DeleteView):
	model = Group
	template_name = 'group/confirm_delete.html'
	success_url = reverse_lazy('group:list')
	login_url = 'user:login'

	def dispatch(self, request, *args, **kwargs):
		group = self.get_object()
		if not group.is_admin(request.user):
			messages.error(request, 'No puedes eliminar este grupo')
			return reverse_lazy('group:list')
		return super().dispatch(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		messages.success(request, 'Grupo eliminado')
		return super().delete(request, *args, **kwargs)

