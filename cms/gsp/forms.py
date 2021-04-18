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

    def __init__(self, *args, **kwargs):
        if "conf_subject_areas" not in kwargs:
            super(PaperSubmissionForm, self).__init__(*args, **kwargs)
        else:
            subject_areas = kwargs.pop('conf_subject_areas')
            SUBJECT_AREAS_CHOICES = [
                (subject_area, subject_area) for subject_area in subject_areas]
            super(PaperSubmissionForm, self).__init__(*args, **kwargs)
            self.fields['subject_area'] = forms.ChoiceField(
                choices=SUBJECT_AREAS_CHOICES)


class AuthorResponseSubmissionForm(forms.ModelForm):

    class Meta:
        model = AuthorResponseSubmission
        exclude = ['title', 'conference',
                   'main_author', 'paper_submission_ref']


class CamPosSubmissionForm(forms.ModelForm):

    class Meta:
        model = CamPosSubmission
        exclude = ['title', 'conference',
                   'main_author', 'paper_submission_ref']
