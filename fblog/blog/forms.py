from django.db import models
from django import forms
from django.forms.models import ModelForm

from .models import Post, Comment


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
