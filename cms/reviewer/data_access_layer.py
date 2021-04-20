from gsp.models import PaperSubmission
from .models import Reviewer, InvitedReviewers, AssignedReviewers
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
    reviewers = []
    reviewer_set = conf.reviewer_set.all()
    for reviewer in reviewer_set:
        reviewers.append(reviewer.user)
    return reviewers


def get_invited_reviewers_of_conf(conf_name):
    conf = conference_dao.get_conference_by_name(conf_name)
    invited_reviewers = []
    invited_reviewer_set = conf.invitedreviewers_set.all()
    for invited_reviewer in invited_reviewer_set:
        invited_reviewers.append(invited_reviewer.user)
    return invited_reviewers


def get_n_invited_reviewers_of_conf_and_subject_area(conf_name, conf_subject_area):
    invited_reviewers = InvitedReviewers.objects.filter(
        conference=conf_name, subject_area=conf_subject_area)
    return len(invited_reviewers)


def get_n_reviewers_of_conf_and_subject_area(conf_name, conf_subject_area):
    reviewers = Reviewer.objects.filter(
        conference=conf_name, area_expertise=conf_subject_area)
    return len(reviewers)


def get_invited_reviewers_emails_of_conf(conf_name):
    conf = conference_dao.get_conference_by_name(conf_name)
    return list(conf.invitedreviewers_set.all().values_list('user', flat=True))


def get_n_reviewers_of_conf_and_subject_area(conf_name, conf_subject_area):
    reviewers = Reviewer.objects.filter(
        conference=conf_name, area_expertise=conf_subject_area)
    return len(reviewers)


def get_number_of_assigned_papers_of_reviewer_in_conf(reviewer, conf_name):
    return AssignedReviewers.objects.filter(reviewer=reviewer, conference=conf_name).count()


def get_all_available_reviewers_of_conf(conf_name):
    reviewers = Reviewer.objects.filter(
        conference=conf_name)
    if len(reviewers) == 0:
        return None
    available_reviewers = []
    for reviewer in reviewers:
        n_assigned_papers = get_number_of_assigned_papers_of_reviewer_in_conf(
            reviewer, conf_name)
        if n_assigned_papers < reviewer.paper_review_limit:
            available_reviewers.append(reviewer)
    if len(available_reviewers) == 0:
        return None
    return available_reviewers
