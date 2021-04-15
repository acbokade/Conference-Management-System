from django.db import models
from conference.models import Conference
from accounts.models import User
from gsp.models import PaperSubmission


class AreaChair(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)


class AssignedAreaChairs(models.Model):
    area_chair = models.ForeignKey(AreaChair, on_delete=models.CASCADE)
    paper_submission = models.ForeignKey(
        PaperSubmission, on_delete=models.CASCADE)
