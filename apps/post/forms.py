from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'content', 'post_type', 'privacy_level', 'image', 'video',
            'link_url', 'link_title', 'link_description', 'subject', 'group', 'tags'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full rounded-md border-gray-300', 'rows': 4, 'required': True, 'minlength': 5}),
            'post_type': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300'}),
            'privacy_level': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300'}),
            'link_url': forms.URLInput(attrs={'class': 'w-full rounded-md border-gray-300'}),
            'link_title': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300'}),
            'link_description': forms.Textarea(attrs={'class': 'w-full rounded-md border-gray-300', 'rows': 3}),
            'tags': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300', 'placeholder': 'tag1, tag2'}),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError('El contenido del post no puede estar vacío')
        if len(content) > 5000:
            raise forms.ValidationError('El contenido es muy largo (máximo 5000 caracteres)')
        if 'http://' in content or 'https://' in content:
            raise forms.ValidationError('Colocá enlaces en los campos correspondientes, no en el contenido.')
        return content
