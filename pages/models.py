# pages.models.py
from django.db import models

# Create your models here.
class Blog(models.Model):
    blog_name = models.CharField(max_length=50, blank=False)
    Blog_body = models.TextField(blank=False)

    def __str__(self):
        return self.blog_name