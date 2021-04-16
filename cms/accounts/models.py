from django.db import models
from django.utils import timezone


class User(models.Model):
    email = models.TextField(null=False, primary_key=True)
    password = models.TextField()
    name = models.TextField()


class ResearchProfile(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person')
    institution = models.CharField(max_length=250)
    research_interests = models.CharField(max_length=500)
    highest_degree = models.CharField(max_length=250)
    google_scholar = models.CharField(max_length=250)


class SecurityQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    question = models.TextField(null=False)
    answer = models.TextField(null=False)
