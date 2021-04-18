from django.shortcuts import render, redirect
from django.contrib import messages
from conference.models import Conference
from conference import data_access_layer as conf_dao
from conference import views as conf_views
from conference import data_access_layer as conference_dao
from reviewer.models import Reviewer
from accounts import utils
from accounts import data_access_layer as accounts_dao
from .models import AreaChair
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

def assign_area_chairs(request, conf_name=None):

    return area_chair_assignment.assign_area_chairs(conf_name)