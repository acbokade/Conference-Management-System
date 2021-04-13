from django import forms
from .models import Reviewer, Review
from conference import utils as conf_utils


class ReviewerForm(forms.ModelForm):
    class Meta:
        model = Reviewer
        exclude = ['user', 'conference']
        widgets = {
            # TODO: multiple select from subject areas of conference
            'area_expertise': forms.TextInput(attrs={'placeholder': 'Enter space separated area expertise'}),
            'paper_review_limit': forms.TextInput(attrs={'placeholder': 'Enter atleast 3 papers to review'})
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ['paper_submission', 'reviewer']
