from django import forms
from django.contrib.auth import authenticate
from apps.user.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username')
        password = cleaned.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Usuario o contraseña incorrectos')
            cleaned['user'] = user
        return cleaned


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_password_confirm(self):
        pw = self.cleaned_data.get('password')
        pwc = self.cleaned_data.get('password_confirm')
        if pw != pwc:
            raise forms.ValidationError('Las contraseñas no coinciden')
        if pw and len(pw) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres')
        return pwc

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
