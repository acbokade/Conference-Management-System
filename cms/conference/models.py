from django.db import models
from cms.accounts.models import User

# Create your models here.
class Conference(models.Model):
    name = models.CharField(null=False, primary_key=True, max_length=250)
    short_name = models.CharField(max_length=100)
    # primary_ca = models.ForeignKey(User)
    ca = models.ManyToManyField(User)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    logo = models.ImageField()
    url = models.URLField()
    # TODO: text choices
    subject_areas = models.TextField(max_length=200)
    expected_submissions = models.IntegerField()
    # ACM_conference_confirmation = models.BooleanField()