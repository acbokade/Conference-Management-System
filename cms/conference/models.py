from django.db import models
from accounts.models import User

# Create your models here.
class Conference(models.Model):
    name = models.CharField(primary_key=True, max_length=250)
    description = models.TextField(blank=True)
    short_name = models.CharField(blank=True, max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create_by')
    created_at = models.DateTimeField(auto_now_add=True)
    ca1_email = models.EmailField(blank=True)
    ca2_email = models.EmailField(blank=True)
    ca3_email = models.EmailField(blank=True)
    ca = models.ManyToManyField(User, related_name='ca') # conference admins
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    logo = models.ImageField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    # TODO: text choices
    subject_areas = models.TextField(max_length=200)
    expected_submissions = models.IntegerField(blank=True)
    is_valid = models.BooleanField() # assigned by portal admin
    # ACM_conference_confirmation = models.BooleanField()

    def __str__(self):
        return self.name