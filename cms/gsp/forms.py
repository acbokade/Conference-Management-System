from django import forms
from django.forms import ValidationError
from .models import PaperSubmission, AuthorResponseSubmission, CamPosSubmission
from . import data_access_layer as conference_dao


class PaperSubmissionForm(forms.ModelForm):

    class Meta:
        model = PaperSubmission
        exclude = ['conference', 'main_author']

    def validate_unique(self):
        pass


class AuthorResponseSubmissionForm(forms.ModelForm):

    class Meta:
        model = AuthorResponseSubmission
        exclude = ['title', 'conference', 'main_author', 'paper_submission_ref']


class CamPosSubmissionForm(forms.ModelForm):

    class Meta:
        model = CamPosSubmission
        exclude = ['title', 'conference', 'main_author', 'paper_submission_ref']
