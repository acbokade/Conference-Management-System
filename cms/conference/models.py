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
    ca_emails = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True)
    paper_submission_deadline = models.DateTimeField(null=True)
    review_submission_deadline = models.DateTimeField(null=True)
    cam_pos_submission_deadline = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    logo = models.ImageField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    # TODO: text choices
    subject_areas = models.TextField(max_length=200)
    expected_submissions = models.IntegerField(blank=True, null=True)
    is_valid = models.BooleanField(default=False)  # assigned by portal admin
    ACM_conference_confirmation = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def clean(self):
        current_datetime = timezone.now()

        if current_datetime > self.start_date:

            raise ValidationError(('Start date %(start_date)s must be set after current date time %(current_datetime)s'),
                                  params={'start_date': self.start_date, 'current_datetime': current_datetime})

        if self.start_date > self.paper_submission_deadline:
            raise ValidationError(('Start date %(start_date)s must be before paper_submission_deadline %(paper_submission_deadline)s'),
                                  params={'start_date': self.start_date, 'paper_submission_deadline': self.paper_submission_deadline})

        if self.paper_submission_deadline > self.review_submission_deadline:
            raise ValidationError(('Paper submission deadline %(paper_submission_deadline)s must be before review submission %(review_submission_deadline)s'),
                                  params={'paper_submission_deadline': self.paper_submission_deadline, 'review_submission_deadline': self.review_submission_deadline})

        if self.review_submission_deadline > self.cam_pos_submission_deadline:
            raise ValidationError(('Review submission deadline %(review_submission_deadline)s must be before Cam Poster submission deadline %(cam_pos_submission_deadline)s'),
                                  params={'review_submission_deadline': self.review_submission_deadline, 'cam_pos_submission_deadline': self.cam_pos_submission_deadline})

        if self.cam_pos_submission_deadline > self.end_date:
            raise ValidationError(('Cam Poster deadline %(cam_pos_submission_deadline)s must be before end date %(end_date)s'),
                                  params={'cam_pos_submission_deadline': self.cam_pos_submission_deadline, 'end_date': self.end_date})


class Conference(ConferenceInfo):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_by')
    ca = models.ManyToManyField(
        User, related_name='ca')  # conference admins

    def __str__(self):
        return self.name


class Workshop(ConferenceInfo):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='workshop_created_by')
    ca = models.ManyToManyField(
        User, related_name='workshop_ca')  # conference admins
    parent_conference_name = models.CharField(max_length=250)
    parent_conference = models.ForeignKey(
        Conference, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
