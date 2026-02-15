from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django import forms
from django.contrib.auth.models import User

from .models import Post, Comment

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class PostForm(forms.ModelForm):
    title = models.CharField()
    content = models.CharField()

    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    content = models.CharField()

    class Meta:
        model = Comment
        fields = ['content']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data['username']
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    def clean(self):
        return self.cleaned_data
