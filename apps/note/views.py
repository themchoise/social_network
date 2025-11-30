from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from apps.note.models import Note
from apps.note.forms import NoteForm


class NoteListView(LoginRequiredMixin, ListView):
	model = Note
	template_name = 'note/list.html'
	context_object_name = 'notes'
	login_url = 'user:login'

	def get_queryset(self):
		qs = Note.objects.select_related('author', 'subject').filter(is_active=True)
		q = self.request.GET.get('q')
		note_type = self.request.GET.get('type')
		if q:
			qs = qs.filter(title__icontains=q)
		if note_type:
			qs = qs.filter(note_type=note_type)
		return qs.order_by('-created_at')


class NoteDetailView(LoginRequiredMixin, DetailView):
	model = Note
	template_name = 'note/detail.html'
	context_object_name = 'note'
	login_url = 'user:login'

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		obj.increment_views()
		return obj


class NoteCreateView(LoginRequiredMixin, CreateView):
	model = Note
	form_class = NoteForm
	template_name = 'note/form.html'
	success_url = reverse_lazy('note:list')
	login_url = 'user:login'

	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, 'Nota creada correctamente')
		return super().form_valid(form)

	def form_invalid(self, form):
		messages.error(self.request, 'Revisá los errores del formulario')
		return super().form_invalid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
	model = Note
	form_class = NoteForm
	template_name = 'note/form.html'
	login_url = 'user:login'

	def get_success_url(self):
		return self.object.get_absolute_url()

	def dispatch(self, request, *args, **kwargs):
		note = self.get_object()
		if note.author != request.user:
			messages.error(request, 'No puedes editar esta nota')
			return reverse_lazy('note:list')
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		messages.success(self.request, 'Nota actualizada')
		return super().form_valid(form)


class NoteDeleteView(LoginRequiredMixin, DeleteView):
	model = Note
	template_name = 'note/confirm_delete.html'
	success_url = reverse_lazy('note:list')
	login_url = 'user:login'

	def dispatch(self, request, *args, **kwargs):
		note = self.get_object()
		if note.author != request.user:
			messages.error(request, 'No puedes eliminar esta nota')
			return reverse_lazy('note:list')
		return super().dispatch(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		messages.success(request, 'Nota eliminada')
		return super().delete(request, *args, **kwargs)

