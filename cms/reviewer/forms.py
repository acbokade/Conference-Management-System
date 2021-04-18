from django import forms
from .models import Reviewer, Review
from conference import utils as conf_utils


class ReviewerForm(forms.ModelForm):
    class Meta:
        model = Reviewer
        exclude = ['user', 'conference']
        widgets = {
            'paper_review_limit': forms.TextInput(attrs={'placeholder': 'Enter atleast 3 papers to review'})
        }

    def __init__(self, *args, **kwargs):
        if "conf_subject_areas" not in kwargs:
            super(ReviewerForm, self).__init__(*args, **kwargs)
        else:
            subject_areas = kwargs.pop('conf_subject_areas')
            SUBJECT_AREA_CHOICES = [
                (subject_area, subject_area) for subject_area in subject_areas]
            super(ReviewerForm, self).__init__(*args, **kwargs)
            self.fields['subject_areas'] = forms.ChoiceField(
                choices=SUBJECT_AREA_CHOICES)


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ['paper_submission', 'reviewer']


class InviteReviewersForm(forms.Form):
    pass

    # def __init__(self, *args, **kwargs):
    #     if "conf_users" not in kwargs:
    #         super(InviteReviewersForm, self).__init__(*args, **kwargs)
    #     else:
    #         conf_users = kwargs.pop('conf_users')
    #         CONF_USERS = [
    #             (conf_user.name, conf_user.name) for conf_user in conf_users]
    #         super(InviteReviewersForm, self).__init__(*args, **kwargs)
    #         self.fields['conference_users'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
    #                                                                     choices=CONF_USERS)
    #         self.fields['research_interests'].widget.attrs['readonly'] = True
