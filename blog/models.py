from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='images/', null=True, blank=False)

    def __str__(self):
        return self.body
