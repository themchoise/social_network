from django.urls import path
from apps.note import views

app_name = 'note'

urlpatterns = [
    path('', views.NoteListView.as_view(), name='list'),
    path('crear/', views.NoteCreateView.as_view(), name='create'),
    path('<int:pk>/', views.NoteDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.NoteUpdateView.as_view(), name='edit'),
    path('<int:pk>/eliminar/', views.NoteDeleteView.as_view(), name='delete'),
]
