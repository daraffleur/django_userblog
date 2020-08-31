from django import forms
from django.forms import models

from blog.models import Post


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PostForm(models.ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'cover']
        labels = {'body': ''}
