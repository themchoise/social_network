from django import forms
from apps.note.models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'title', 'content', 'subject', 'note_type', 'privacy_level', 'tags', 'file_attachment'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300', 'required': True}),
            'content': forms.Textarea(attrs={'class': 'w-full rounded-md border-gray-300', 'rows': 6, 'required': True}),
            'subject': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300'}),
            'note_type': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300'}),
            'privacy_level': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300'}),
            'tags': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300', 'placeholder': 'django, redes'}),
            'file_attachment': forms.ClearableFileInput(attrs={'class': 'w-full'})
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('El título debe tener al menos 3 caracteres')
        return title

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags and len(tags) > 500:
            raise forms.ValidationError('Demasiados tags')
        return tags
