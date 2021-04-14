from gsp.models import PaperSubmission
from .models import Reviewer
from conference import data_access_layer as conference_dao


def get_review_by_paper_title_and_reviewer(title, reviewer_email):
    paper_submission = PaperSubmission.objects.get(title=title)
    for review in paper_submission.review_set.all():
        if review.reviewer.email == reviewer_email:
            return review
    return None


def get_reviewer_by_email(email):
    reviewer = Reviewer.objects.filter(user=email)[0]
    return reviewer


def get_all_reviewers_of_conf(conf_name):
    conf = conference_dao.get_conference_by_name(conf_name)
    return list(conf.reviwers_set.all())
