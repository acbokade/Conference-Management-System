from django.db import models
from accounts.models import User
from conference.models import Conference
from django.core.validators import MinValueValidator


class Reviewer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    conference = models.ForeignKey(
        Conference, on_delete=models.CASCADE)
    prior_reviewing_experience = models.CharField(max_length=250)
    prior_research_paper_submissions = models.PositiveIntegerField()
    area_expertise = models.CharField(max_length=250)
    paper_review_limit = models.PositiveIntegerField(
        validators=[MinValueValidator(3)])

    def __str__(self):
        return self.user.name


class Review(models.Model):
    paper = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.paper.name
