from django import forms
from .models import Reviewer, Review
from conference import utils as conf_utils


class ReviewerForm(forms.ModelForm):
    class Meta:
        model = Reviewer
        exclude = ['user', 'conference']
        widgets = {
            # TODO: multiple select from subject areas of conference
            'paper_review_limit': forms.TextInput(attrs={'placeholder': 'Enter atleast 3 papers to review'})
        }

    def __init__(self, *args, **kwargs):
        if "conf_subject_areas" not in kwargs:
            super(ReviewerForm, self).__init__(*args, **kwargs)
        else:
            subject_areas = kwargs.pop('conf_subject_areas')
            RESEARCH_EXPERTISE_CHOICES = [
                (subject_area, subject_area) for subject_area in subject_areas]
            super(ReviewerForm, self).__init__(*args, **kwargs)
            self.fields['area_expertise'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                                      choices=RESEARCH_EXPERTISE_CHOICES)


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ['paper_submission', 'reviewer']
