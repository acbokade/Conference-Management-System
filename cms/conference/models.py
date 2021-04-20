from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class ConferenceInfo(models.Model):
    name = models.CharField(primary_key=True, max_length=250)
    description = models.TextField(blank=True)
    short_name = models.CharField(blank=True, max_length=125)
    location = models.CharField(blank=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    ca_emails = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True)
    paper_submission_deadline = models.DateTimeField(null=True)
    review_submission_deadline = models.DateTimeField(null=True)
    cam_pos_submission_deadline = models.DateTimeField(
        null=True)
    ac_decision_start_date = models.DateTimeField(null=True)
    ac_decision_submission_deadline = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    logo = models.ImageField(null=True, blank=True, upload_to='images')
    url = models.URLField(null=True, blank=True)
    subject_areas = models.TextField(max_length=200)
    expected_submissions = models.IntegerField(blank=True, null=True)
    is_valid = models.BooleanField(default=False)  # assigned by portal admin
    ACM_conference_confirmation = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def clean(self):
        current_datetime = timezone.now()
        # checking this condition only while creation of conference not updation
        if not self.updated_at and current_datetime > self.start_date:
            raise ValidationError(('Start date %(start_date)s must be set after current date time %(current_datetime)s'),
                                  params={'start_date': self.start_date, 'current_datetime': current_datetime})

        if self.start_date > self.paper_submission_deadline:
            raise ValidationError(('Start date %(start_date)s must be before paper_submission_deadline %(paper_submission_deadline)s'),
                                  params={'start_date': self.start_date, 'paper_submission_deadline': self.paper_submission_deadline})

        if self.paper_submission_deadline > self.review_submission_deadline:
            raise ValidationError(('Paper submission deadline %(paper_submission_deadline)s must be before review submission %(review_submission_deadline)s'),
                                  params={'paper_submission_deadline': self.paper_submission_deadline, 'review_submission_deadline': self.review_submission_deadline})

        if self.review_submission_deadline > self.ac_decision_start_date:
            raise ValidationError(('Review submission deadline %(review_submission_deadline)s must be before Area Chair Decision start date %(ac_decision_start_date)s'),
                                  params={'review_submission_deadline': self.review_submission_deadline, 'ac_decision_start_date': self.ac_decision_start_date})

        if self.ac_decision_start_date > self.ac_decision_submission_deadline:
            raise ValidationError(('Area Chair Decision start date %(ac_decision_start_date)s must be before Area Chair Decision deadline %(ac_decision_submission_deadline)s'),
                                  params={'ac_decision_start_date': self.ac_decision_start_date, 'ac_decision_submission_deadline': self.ac_decision_submission_deadline})

        if self.ac_decision_submission_deadline > self.cam_pos_submission_deadline:
            raise ValidationError(('Area Chair Decision deadline %(ac_decision_submission_deadline)s must be before Camera Ready and Poster Submission %(cam_pos_submission_deadline)s'),
                                  params={'ac_decision_submission_deadline': self.ac_decision_submission_deadline, 'cam_pos_submission_deadline': self.cam_pos_submission_deadline})

        if self.cam_pos_submission_deadline > self.end_date:
            raise ValidationError(('Cam Poster deadline %(cam_pos_submission_deadline)s must be before end date %(end_date)s'),
                                  params={'cam_pos_submission_deadline': self.cam_pos_submission_deadline, 'end_date': self.end_date})

    @property
    def logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return "/static/images/no_logo.png"


class Conference(ConferenceInfo):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_by')
    ca = models.ManyToManyField(
        User, related_name='ca')  # conference admins

    def __str__(self):
        return self.name
