from .models import AreaChair, AreaChairDecision
from gsp.models import PaperSubmission


def get_ac_by_email_and_conf(email, conf_name):
    ac = AreaChair.objects.filter(user=email, conference=conf_name)[0]
    return ac


def get_ac_decision_by_paper_title_and_area_chair(title, area_chair):
    paper_submission = PaperSubmission.objects.get(title=title)
    ac_decision = AreaChairDecision(paper_submission=paper_submission, area_chair=area_chair)
    return ac_decision
