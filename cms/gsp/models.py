from django.db import models
from accounts.models import User
from conference.models import Conference


class ConferenceSubmission(models.Model):

    conference = models.ForeignKey(
        Conference, on_delete=models.CASCADE, null=True, blank=False
    )
    title = models.CharField(primary_key=True, max_length=50, blank=False, default='')
    main_author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=False
    )

    class Meta:
        abstract = True


class PaperSubmission(ConferenceSubmission):

    abstract = models.TextField(blank=False)
    pdf_paper = models.FileField(
        upload_to='tmp/cms-project/main_paper', blank=False, null=True)
    supplementary_material = models.FileField(
        upload_to='tmp/cms-project/supplementary', null=True, blank=True, default=None)
    other_authors_emails = models.TextField(blank=True)
    
    subject_area = models.CharField(max_length=250)
    authors = models.ManyToManyField(User, related_name='authors')

    def __str__(self):
        return self.title


class AuthorResponseSubmission(models.Model):
    response_pdf = models.FileField(
        upload_to='tmp/cms-project/responses', blank=True, null=True)
    paper_submission_ref = models.ForeignKey(
        PaperSubmission, on_delete=models.CASCADE, null=False, blank=True
    )


class CamPosSubmission(models.Model):
    camera_ready_pdf = models.FileField(
        upload_to='tmp/cms-project/camera', blank=False)
    poster_pdf = models.FileField(
        upload_to='tmp/cms-project/posters', blank=False)
    paper_submission_ref = models.ForeignKey(
        PaperSubmission, on_delete=models.CASCADE, null=False, blank=True
    )
