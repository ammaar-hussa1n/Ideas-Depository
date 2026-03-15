from django.db import models

# Create your models here.


class Idea(models.Model):
    idea_title = models.CharField(max_length=200)
    idea_description = models.TextField()
    idea_time = models.DateTimeField(auto_now_add=True)
