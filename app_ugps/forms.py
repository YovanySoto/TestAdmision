from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomRegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre de usuario"
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Nombre"
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Apellido"
    )
    email = forms.EmailField(
        required=True,
        label="Correo electrónico"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmar contraseña"
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya existe")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden")
        
        return cleaned_data
    

    