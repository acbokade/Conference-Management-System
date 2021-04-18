from django import forms
from .models import AreaChair, AreaChairDecision


class AreaChairDecisionForm(forms.ModelForm):
    class Meta:
        model = AreaChairDecision
        exclude = ['paper_submission', 'area_chair']
