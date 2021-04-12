from django.db import models
from accounts.models import User

# Create your models here.
class ConferenceSubmission(models.Model):
    paper_index = None

    class Meta:
        abstract = True
        
    def __str__(self):
        return str(paper_index) 


class PaperSubmission(ConferenceSubmission):

    title = models.CharField(primary_key=True, max_length=50)
    abstract = models.TextField(blank=False)
    pdf_paper = models.FileField(upload_to='tmp/cms-project/main_paper', blank=False)
    supplementary_material = models.FileField(upload_to='tmp/cms-project/supplementary', null=True, blank=True, default=None)

    author_list = models.TextField(blank=False)

    def __str__(self):
        return self.title

class AuthorResponseSubmission(ConferenceSubmission):
    response_pdf = models.FileField(upload_to='tmp/cms-project/responses', blank=True, null=True)

class CamPosSubmission(ConferenceSubmission):
    camera_ready_pdf = models.FileField(upload_to='tmp/cms-project/camera', blank=False)
    poster_pdf = models.FileField(upload_to='tmp/cms-project/posters', blank=False)

