from django.shortcuts import render, redirect
from .models import Reviewer
from .forms import ReviewerForm, ReviewForm
from accounts import utils
from . import data_access_layer as reviewer_dao
from accounts import data_access_layer as accounts_dao
from conference import data_access_layer as conference_dao
from gsp import data_access_layer as gsp_dao
from conference import views as conf_views


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
        form = ReviewerForm()
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
            return redirect()
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
            review.paper_submission = gsp_dao.get_paper_submission_by_title(
                title)
            review.save()
            return redirect()
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
            return redirect()
        return render(request, "make_review.html", {"is_logged_in": is_logged_in, "form": form})


def reviewer_assignment(request):
    pass
