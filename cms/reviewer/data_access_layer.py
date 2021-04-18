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


def get_reviewer_by_email_and_conf(email, conf_name):
    reviewer = Reviewer.objects.filter(user=email, conference=conf_name)[0]
    return reviewer


def get_all_reviewers_of_conf(conf_name):
    conf = conference_dao.get_conference_by_name(conf_name)
    return list(conf.reviwers_set.all())


def get_invited_reviewers_emails_of_conf(conf_name):
    conf = conference_dao.get_conference_by_name(conf_name)
    invited_reviewers = conf.invitedreviewers_set.all()
    invited_reviewers_email_list = [
        invited_reviewer.user.email for invited_reviewer in invited_reviewers]
    return invited_reviewers_email_list
