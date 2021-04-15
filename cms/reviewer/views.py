from django.shortcuts import render, redirect
from .models import Reviewer, InvitedReviewers
from .forms import ReviewerForm, ReviewForm, InviteReviewersForm
from accounts import utils
from . import data_access_layer as reviewer_dao
from accounts import data_access_layer as accounts_dao
from conference import data_access_layer as conference_dao
from gsp import data_access_layer as gsp_dao
from conference import views as conf_views
from .utils import assign_reviewers


def redirect_signup(request):
    return redirect('/accounts/signup')


def redirect_login(request):
    return redirect('/accounts/login')


def redirect_logout(request):
    return redirect('/accounts/logout')


def redirect_userpage(request):
    return redirect('/accounts/userpage')


def apply_as_a_reviewer(request, conf_name):
    is_logged_in = utils.check_login(request)
    if request.method == "GET":
        conf = conference_dao.get_conference_by_name(conf_name)
        conf_subject_areas = conf.subject_areas.split(',')
        form = ReviewerForm(conf_subject_areas=conf_subject_areas)
        return render(request, "apply_as_a_reviewer.html", {"is_logged_in": is_logged_in, "form": form, "name": conf_name})
    if request.method == "POST":
        form = ReviewerForm(request.POST)
        if form.is_valid():
            reviewer = form.save(commit=False)
            reviewer.conference = conference_dao.get_conference_by_name(
                conf_name)
            reviewer.user = accounts_dao.obtain_user_by_email(
                request.COOKIES.get('email'))
            reviewer.save()
            return redirect(conf_views.list_conferences)
        return render(request, "apply_as_a_reviewer.html", {"is_logged_in": is_logged_in, "form": form, "name": conf_name})


def make_review(request, conf_name, title):
    is_logged_in = utils.check_login(request)
    if request.method == "GET":
        form = ReviewForm()
        return render(request, "make_review.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            # TODO: prevent any user from making review
            review.reviewer = reviewer_dao.get_reviewer_by_email(
                request.COOKIES.get('email'))
            paper_submissions = subject_area_submissions_dict[subject_area] = reviewer_dao.get_reviewer_by_email(
                request.COOKIES.get('email'))
            review.paper_submission = gsp_dao.get_paper_submission_by_title(
                title)
            review.save()
            return redirect(conf_views.list_conferences)
        return render(request, "make_review.html", {"is_logged_in": is_logged_in, "form": form})


def edit_review(request, conf_name, title):
    is_logged_in = utils.check_login(request)
    if request.method == "GET":
        reviewer_email = request.COOKIES.get('email')
        review = reviewer_dao.get_review_by_paper_title_and_reviewer(
            title, reviewer_email)
        form = ReviewForm(instance=review)
        return render(request, "edit_review.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            # TODO: prevent any user from editing review
            review.reviewer = reviewer_dao.get_reviewer_by_email(
                request.COOKIES.get('email'))
            review.paper_submission = gsp_dao.get_paper_submission_by_title(
                title)
            review.save()
            return redirect(conf_views.list_conferences)
        return render(request, "make_review.html", {"is_logged_in": is_logged_in, "form": form})


def automated_reviewer_assignment(request, conf_name):
    reviwers_list = reviewer_dao.get_all_reviewers_of_conf(conf_name)
    paper_submissions_list = gsp_dao.get_all_paper_submissions_of_conf(
        conf_name)

    conf_subject_areas = conference_dao.get_conference_subject_areas()

    subject_area_reviewer_dict = {}
    for reviewer in reviwers_list:
        subject_area_reviewer_dict[reviewer.area_expertise] = reviewer

    subject_area_submissions_dict = {}
    for paper_submission in paper_submissions_list:
        subject_area_submissions_dict[paper_submission.subject_area] = paper_submission

    # reviewer assignment done for each subject area independently
    for subject_area in conf_subject_areas:
        reviewers = subject_area_reviewer_dict[subject_area]
        paper_submissions = subject_area_submissions_dict[subject_area]
        paper_reviewer_mapping = assign_reviewers(reviewers, paper_submissions)


def invite_reviewers(request, conf_name):
    is_logged_in = utils.check_login(request)
    conf = conference_dao.get_conference_by_name(conf_name)
    if request.method == "GET":
        all_conf_paper_submissions = conf.papersubmission_set.all()
        conf_users = set()
        for paper_submission in all_conf_paper_submissions:
            conf_users.add(paper_submission.main_author)
        conf_users = list(conf_users)
        # form = InviteReviewersForm(conf_users=conf_users)
        # print(form.fields['conference_users'].choices)
        return render(request, "invite_reviewers.html", {"is_logged_in": is_logged_in, "conf_users": conf_users})
    if request.method == "POST":
        selected_users_emails = request.POST.getlist('checked_users')
        for selected_user_email in selected_users_emails:
            selected_user = accounts_dao.obtain_user_by_email(
                selected_user_email)
            invited_reviewer = InvitedReviewers.objects.create(
                user=selected_user, conference=conf)
            invited_reviewer.save()
        # send emails to invited reviewers
        return redirect(conf_views.list_conferences)
