from django import forms
from django.forms import ValidationError
from .models import Conference
from .constants import *
from datetime import datetime
from . import data_access_layer as conference_dao


class DateInput(forms.DateInput):
    input_type = 'date'


def check_date_validations(cleaned_data):
    start_date = cleaned_data.get('start_date')
    end_date = cleaned_data.get('end_date')
    paper_submission_deadline = cleaned_data.get(
        'paper_submission_deadline')
    review_submission_deadline = cleaned_data.get(
        'review_submission_deadline')
    cam_pos_submission_deadline = cleaned_data.get(
        'cam_pos_submission_deadline')

    # paper submission deadline within two months of creation date
    submission_creation_diff = paper_submission_deadline - \
        start_date
    if (submission_creation_diff.days > PAPER_SUBMISSION_CREATION_DIFF):
        raise ValidationError(f"Paper submission deadline must be within \
                                    {PAPER_SUBMISSION_CREATION_DIFF} days of creation date")

    # review and paper submission deadline difference
    review_paper_submission_diff = review_submission_deadline - \
        paper_submission_deadline
    if(review_paper_submission_diff.days > REVIEW_PAPER_SUBMISSION_DIFF):
        raise ValidationError(f"Review submission deadline must be within \
                                    {REVIEW_PAPER_SUBMISSION_DIFF} days of paper submission deadline")

    # cam_pos and review submission deadline difference
    cam_pos_review_submission_diff = cam_pos_submission_deadline - \
        review_submission_deadline
    if(cam_pos_review_submission_diff.days > CAM_POS_REVIEW_SUBMISSION_DIFF):
        raise ValidationError(f"CAM POS submission deadline must be within \
                                    {CAM_POS_REVIEW_SUBMISSION_DIFF} days of review submission deadline")

    # end_date and cam_pos_submission deadline difference
    end_cam_pos_submission_diff = end_date - cam_pos_submission_deadline
    if(end_cam_pos_submission_diff.days > END_CAM_POS_SUBMISSION_DIFF):
        raise ValidationError(f"End date must be within \
                                    {END_CAM_POS_SUBMISSION_DIFF} days of CAM POS submission deadline")

    return cleaned_data


form_widgets = {
    'start_date': DateInput(),
    'end_date': DateInput(),
    'paper_submission_deadline': DateInput(),
    'review_submission_deadline': DateInput(),
    'cam_pos_submission_deadline': DateInput(),
    'ac_decision_start_date': DateInput(),
    'ac_decision_submission_deadline': DateInput(),
    'ca_emails': forms.TextInput(attrs={'placeholder': 'Enter space separated emails of conference admins eg. a@gmail.com b@gmail.com,...'}),
    'location': forms.TextInput(attrs={'placeholder': 'Enter city and country'}),
    'subject_areas': forms.TextInput(attrs={'placeholder': 'Enter comma separated subject areas eg. Segmentation,Adversarial Networks,Recurrent Networks'})
}


class ConferenceForm(forms.ModelForm):

    def validate_unique(self):
        pass

    class Meta:
        model = Conference
        exclude = ['is_valid', 'ca', 'created_by']
        widgets = form_widgets

    def clean(self):
        cleaned_data = super(ConferenceForm, self).clean()
        # checking dates validation
        cleaned_data = check_date_validations(cleaned_data)
