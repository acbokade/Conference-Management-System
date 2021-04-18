from django.shortcuts import render, redirect
from django.contrib import messages
from conference.models import Conference
from conference import data_access_layer as conf_dao
from conference import views as conf_views
from conference import data_access_layer as conference_dao
from reviewer.models import Reviewer
from accounts import utils
from django.utils import timezone
from accounts import data_access_layer as accounts_dao
from .models import AreaChair, AssignedAreaChairs
from .forms import AreaChairDecisionForm
from . import data_access_layer as area_chair_dao
from gsp import data_access_layer as gsp_dao
from . import area_chair_assignment

def redirect_signup(request):
    return redirect('/accounts/signup')


def redirect_login(request):
    return redirect('/accounts/login')


def redirect_logout(request):
    return redirect('/accounts/logout')


def redirect_userpage(request):
    return redirect('/accounts/userpage')


def select_area_chair(request, conf_name):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        cur_user_email = request.COOKIES.get('email')
        # check if user is CA of the conference or not
        conf_ca_emails = conference_dao.get_a_conference_ca_emails(conf_name)
        if cur_user_email not in conf_ca_emails:
            messages.error(
                request, f"Sorry, you are not a conference admin for {conf_name} conference")
            redirect(conf_views.list_conferences)
        conf = conf_dao.get_conference_by_name(conf_name)
        if request.method == "POST":
            selected_area_chair_emails = request.POST.getlist('checked_users')
            for selected_area_chair_email in selected_area_chair_emails:
                selected_user = accounts_dao.obtain_user_by_email(
                    selected_area_chair_email)
                area_chair = AreaChair.objects.create(
                    user=selected_user, conference=conf)
                area_chair.save()
            # TODO: send emails to invited reviewers
            return redirect(conf_views.list_conferences)
        else:
            # reviewers of conf_name conference
            conf_reviewers = Reviewer.objects.filter(conference=conf_name)
            area_expertise_reviwer_dict = {}
            for conf_reviewer in conf_reviewers:
                area_expertise = conf_reviewer.area_expertise
                if area_expertise not in area_expertise_reviwer_dict:
                    area_expertise_reviwer_dict[area_expertise] = [
                        conf_reviewer]
                else:
                    area_expertise_reviwer_dict[area_expertise].append(
                        conf_reviewer)
        return render(request, "select_area_chair.html",
                      {"in_logged_in": is_logged_in, "area_expertise_reviwer_dict": area_expertise_reviwer_dict})
    return redirect('/accounts/login')

<<<<<<< HEAD
def assign_area_chairs(request, conf_name=None):

    return area_chair_assignment.assign_area_chairs(conf_name)
=======

def make_ac_decision(request, conf_name, title):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        cur_user_email = request.COOKIES.get('email')
        # check if reviewer is assigned to review the paper
        try:
            area_chair = AreaChair.objects.get(
                user=cur_user_email, conference=conf_name)
        except:
            messages.error(
                request, f"Sorry, you are not an Area Chair for {conf_name} conference")
            redirect(conf_views.list_conferences)
        try:
            paper_submission = gsp_dao.get_paper_submission_by_title(
                title)
        except:
            messages.error(
                request, f"Paper {title} doesn't exist")
            redirect(conf_views.list_conferences)
        try:
            assigned_ac_found = AssignedAreaChairs.objects.find(area_chair=area_chair,
                                                                     paper_submission=paper_submission)
        except:
            messages.error(
                request, f"Sorry, you are not an Area Chair for {title} paper")
            redirect(conf_views.list_conferences)

        # review submission deadline check
        conf = conference_dao.get_conference_by_name(conf_name)
        cur_time = timezone.now()

        if cur_time < conf.ac_decision_start_date:
            messages.error(
                request, f"Sorry, AC Decision submissions have not started yet")
            redirect(conf_views.list_conferences)

        if cur_time > conf.ac_decision_submission_deadline:
            messages.error(
                request, f"Sorry, AC Decision submission deadline has been elapsed")
            redirect(conf_views.list_conferences)

        if request.method == "POST":
            form = AreaChairDecisionForm(request.POST)
            if form.is_valid():
                ac_decision = form.save(commit=False)
                ac_decision.area_chair = area_chair_dao.get_ac_by_email_and_conf(
                    request.COOKIES.get('email'), conf_name)
                # paper_submissions = subject_area_submissions_dict[subject_area] = reviewer_dao.get_reviewer_by_email(
                #     request.COOKIES.get('email'))
                ac_decision.paper_submission = gsp_dao.get_paper_submission_by_title(
                    title)
                ac_decision.save()
                return redirect(conf_views.list_conferences)
        else:
            form = AreaChairDecisionForm()
        return render(request, "make_ac_decision.html", {"is_logged_in": is_logged_in, "form": form})
    return redirect('/accounts/login')


def edit_ac_decision(request, conf_name, title):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        cur_user_email = request.COOKIES.get('email')
        # check if area chair is assigned to make decision for the paper
        try:
            area_chair = AreaChair.objects.get(
                user=cur_user_email, conference=conf_name)
        except:
            messages.error(
                request, f"Sorry, you are not an Area Chair for {conf_name} conference")
            redirect(conf_views.list_conferences)
        try:
            paper_submission = gsp_dao.get_paper_submission_by_title(
                title)
        except:
            messages.error(
                request, f"Paper {title} doesn't exist")
            redirect(conf_views.list_conferences)
        try:
            assigned_ac_found = AssignedAreaChairs.objects.find(area_chair=area_chair,
                                                                paper_submission=paper_submission)
        except:
            messages.error(
                request, f"Sorry, you are not an Area Chair for {title} paper")
            redirect(conf_views.list_conferences)

        # review submission deadline check
        conf = conference_dao.get_conference_by_name(conf_name)
        cur_time = timezone.now()

        if cur_time < conf.ac_decision_start_date:
            messages.error(
                request, f"Sorry, AC Decision submissions have not started yet")
            redirect(conf_views.list_conferences)

        if cur_time > conf.ac_decision_submission_deadline:
            messages.error(
                request, f"Sorry, AC Decision submission deadline has been elapsed")
            redirect(conf_views.list_conferences)

        ac_decision = area_chair_dao.get_ac_decision_by_paper_title_and_area_chair(
            title, area_chair)
        if request.method == "POST":
            form = AreaChairDecisionForm(request.POST, instance=ac_decision)
            if form.is_valid():
                ac_decision = form.save(commit=False)
                ac_decision.save()
                return redirect(conf_views.list_conferences)
            return render(request, "edit_ac_decision.html", {"is_logged_in": is_logged_in, "form": form})
        else:
            form = AreaChairDecisionForm(instance=ac_decision)
        return render(request, "edit_ac_decision.html", {"is_logged_in": is_logged_in, "form": form})
    return redirect('/accounts/login')
>>>>>>> main
