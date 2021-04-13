from django import forms
from django.forms import ValidationError
from .models import Conference, Workshop
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
    'ca_emails': forms.TextInput(attrs={'placeholder': 'Enter space separated emails of conference admins eg. a@gmail.com b@gmail.com,...'}),
    'location': forms.TextInput(attrs={'placeholder': 'Enter city and country'})
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


class WorkshopForm(forms.ModelForm):

    def validate_unique(self):
        pass

    class Meta:
        model = Workshop
        exclude = ['is_valid', 'ca', 'parent_conference', 'created_by']
        widgets = form_widgets

    def clean(self):
        cleaned_data = super(WorkshopForm, self).clean()

        # checking validity of parent conference
        parent_conf_name = cleaned_data['parent_conference_name']
        all_conf_names = conference_dao.get_all_conferences_names()
        if parent_conf_name not in all_conf_names:
            raise ValidationError(
                f"Parent conference name {parent_conf_name} is not valid")

        # checking dates validation
        check_date_validations(cleaned_data)

        # checking ca emails validation
        parent_conf_ca_emails = set(conference_dao.get_a_conference_ca_emails(
            parent_conf_name))
        workshop_ca_emails = set(cleaned_data['ca_emails'].split())
        if parent_conf_ca_emails != workshop_ca_emails:
            raise ValidationError(
                "Entered Ca emails are not same as that of parent conference")
