from django.db import models
from django.contrib.auth.models import User

class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    idea_title = models.CharField(max_length=200)
    idea_description = models.TextField()
    idea_time = models.DateTimeField(auto_now_add=True)
