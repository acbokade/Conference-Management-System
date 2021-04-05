from django.db import models
from django.utils import timezone


class User(models.Model):
    email = models.TextField(null=False, primary_key=True)
    password = models.TextField()
    name = models.TextField()
