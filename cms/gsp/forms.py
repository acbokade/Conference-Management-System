from django import forms
from django.forms import ValidationError
from .models import PaperSubmission, AuthorResponseSubmission, CamPosSubmission
from . import data_access_layer as conference_dao

import django.core.files.uploadedfile as uploadedfile


class PaperSubmissionForm(forms.ModelForm):

    class Meta:
        model = PaperSubmission
        exclude = ['conference', 'main_author', 'authors']

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
    
    def clean(self):
        cleaned_data = super(PaperSubmissionForm, self).clean()
        cleaned_data = self.validate_form(cleaned_data)

    def validate_form(self, data):

        paper_file = data.get('pdf_paper')
        if isinstance(paper_file, uploadedfile.InMemoryUploadedFile):
            paper_file_name = data.get('pdf_paper')._name
            if not paper_file_name.endswith('.pdf'):
                raise ValidationError(f'Only PDF files are accepted, got {paper_file_name}')


class AuthorResponseSubmissionForm(forms.ModelForm):

    class Meta:
        model = AuthorResponseSubmission
        exclude = ['paper_submission_ref']


class CamPosSubmissionForm(forms.ModelForm):

    class Meta:
        model = CamPosSubmission
        exclude = ['paper_submission_ref']
