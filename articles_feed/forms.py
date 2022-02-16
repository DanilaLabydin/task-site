from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.validators import EmailValidator

from .models import *
from django.core.exceptions import ValidationError


class AddArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Not selected"

    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError
        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(validators=[EmailValidator()], label='email',
                             widget=forms.EmailInput(attrs={'class': 'form-input'}),)
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='password again', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    groups = forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'groups')

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Account with this email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=username).exists():
            raise ValidationError('Account with this email already exists')
        return username


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
