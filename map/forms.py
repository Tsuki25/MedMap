from django import forms
from .models import Usuario

class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail", max_length=120, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))