from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'content', 'post_type', 'privacy_level', 'image', 'video',
            'link_url', 'link_title', 'link_description', 'subject', 'group', 'tags'
        ]

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError('El contenido del post no puede estar vacío')
        if len(content) > 5000:
            raise forms.ValidationError('El contenido es muy largo (máximo 5000 caracteres)')
        return content
