from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'required': 'true'}))
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'input',  'type': 'email', 'required': 'true'}))
    password1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input',  'type': 'password', 'required': 'true'}))
    password2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input', 'type': 'password', 'required': 'true'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
