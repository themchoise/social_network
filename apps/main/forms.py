from django import forms

class FeedbackForm(forms.Form):
    asunto = forms.CharField(
        label="Asunto",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-md border-gray-300",
            "placeholder": "Breve título",
            "required": True,
            "minlength": 3,
        }),
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "w-full rounded-md border-gray-300",
            "placeholder": "tu@email.com",
            "required": True,
        }),
    )
    mensaje = forms.CharField(
        label="Mensaje",
        required=True,
        min_length=10,
        widget=forms.Textarea(attrs={
            "class": "w-full rounded-md border-gray-300",
            "rows": 4,
            "placeholder": "Contanos tu idea o problema...",
            "required": True,
            "minlength": 10,
        }),
    )

    def clean_asunto(self):
        asunto = self.cleaned_data.get("asunto", "")
        if any(bad in asunto.lower() for bad in ["spam", "viagra", "casino"]):
            raise forms.ValidationError("El asunto contiene palabras no permitidas.")
        return asunto

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get("mensaje", "")
        if mensaje.strip().lower() == mensaje.strip().upper():
            # ejemplo tonto: todo mayúsculas
            raise forms.ValidationError("Evita escribir todo en mayúsculas.")
        return mensaje
