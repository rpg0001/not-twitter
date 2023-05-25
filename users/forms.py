from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'required': 'true',
        'placeholder': 'Enter username'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'input',
        'type': 'email',
        'required': 'true',
        'placeholder': 'Enter email address'
    }))
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'type': 'password',
        'required': 'true',
        'placeholder': 'Enter password'
    }))
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'type': 'password',
        'required': 'true',
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    display_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'type': 'text',
    }))
    bio = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'input',
        'type': 'text',
    }))
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'type': 'text',
    }))

    class Meta:
        model = Profile
        fields = ('display_name', 'bio', 'location')
