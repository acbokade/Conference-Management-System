from django import forms
from django.forms import ValidationError
from .models import PaperSubmission, AuthorResponseSubmission, CamPosSubmission
from datetime import datetime
from . import data_access_layer as conference_dao

class DateInput(forms.DateInput):
    input_type = "date"

# form_widgets = {
#     'title': forms.TextInput(attrs={
#         'placeholder': 'Paper Title'
#     })
# }


class PaperSubmissionForm(forms.ModelForm):

    # title = forms.CharField(max_length=50)
    # paper_pdf = forms.FileField()

    class Meta:
        model = PaperSubmission
        # fields = ['title']
        exclude = ['submission_index']
        # widgets = form_widgets

    def clean(self):
        cleaned_data = super(PaperSubmissionForm, self).clean()
        cleaned_data = validate_paper_submission_form(cleaned_data)

class AuthorResponseSubmissionForm(forms.ModelForm):

    class Meta:
        model = AuthorResponseSubmission
        exclude = []
        # widgets = form_widgets

    def clean(self):
        pass

class CamPosSubmissionForm(forms.ModelForm):

    class Meta:
        model = CamPosSubmission
        exclude = []
        # widgets = form_widgets

    def clean(self):
        pass