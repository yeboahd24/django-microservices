from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author_id = models.IntegerField(null=True, blank=True, default=0, unique=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
