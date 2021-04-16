from django.shortcuts import render, redirect
from django.contrib import messages
from accounts import utils
from datetime import datetime
from . import models
from accounts import models as accounts_models
from gsp import models as gsp_models
from accounts import views as account_views
from .forms import ConferenceForm, WorkshopForm
from . import utils as conf_utils
from . import data_access_layer as conference_dao
from accounts import data_access_layer as accounts_dao
# from accounts import data_access_layer as accounts_dao


def redirect_signup(request):
    return redirect('/accounts/signup')


def redirect_login(request):
    return redirect('/accounts/login')


def redirect_logout(request):
    return redirect('/accounts/logout')


def redirect_userpage(request):
    return redirect('/accounts/userpage')


def redirect_assigned_papers(request):
    return redirect('/reviewer/assigned_papers')


def list_conferences(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        confs = conference_dao.get_all_conferences()
        workshops = conference_dao.get_all_workshops()
        is_ca_confs = conf_utils.obtain_ca_boolean_array(request.COOKIES.get('email'), confs)
        is_invited_as_revs = conf_utils.obtain_invited_rev_boolean_array(request.COOKIES.get('email'), confs)
        assert len(confs) == len(is_ca_confs) == len(is_invited_as_revs)

        confs_list = zip(confs, is_ca_confs, is_invited_as_revs)
        return render(request, "list_conferences.html", {"is_logged_in": is_logged_in, "confs_list": confs_list,
                                                    "workshops": workshops})
    return redirect('/accounts/')


def list_my_conferences(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        author = accounts_dao.obtain_user_by_email(request.COOKIES.get('email'))
        conf_submissions = gsp_models.PaperSubmission.objects.all().filter(main_author=author)
        confs = [subm.conference for subm in conf_submissions]

        # Write code to obtain workshop submission
        # workshops = gsp_models.PaperSubmission.objects.get(main_author=author)
        workshops = None

        return render(request, "list_my_conferences.html", {"is_logged_in": is_logged_in,
                                                         "confs": confs, "workshops": workshops})
    return redirect('/accounts/')


def create_conference(request):
    is_logged_in = utils.check_login(request)
    if request.method == "GET":
        form = ConferenceForm()
        return render(request, "create_conference.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        form = ConferenceForm(request.POST)
        if form.is_valid():
            conference = form.save(commit=False)

            ca_emails = request.POST.get('ca_emails')
            # adding creator's email to ca_emails
            creator_email = request.COOKIES.get('email')
            conference.created_by = accounts_dao.obtain_user_by_email(
                creator_email)
            ca_emails += f" {creator_email}"
            conference.ca_emails = ca_emails
            conference.save()
            ca_emails = ca_emails.split()
            for ca_email in ca_emails:
                try:
                    other_ca = accounts_dao.obtain_user_by_email(ca_email)
                    conference.ca.add(other_ca)
                except accounts_models.User.DoesNotExist:
                    # TODO: handle this event by sending email to creator indicating that the email doesnt exist
                    pass
            messages.success(request, 'Conference succesfully created')
            return redirect(list_conferences)
        else:
            return render(request, "create_conference.html", {"form": form})
        # afterwards portal admin validates it and sets is_valid field accordingly


def update_conference(request, name):
    is_logged_in = utils.check_login(request)
    conf = conference_dao.get_conference_by_name(name)
    if request.method == "GET":
        cur_user_email = request.COOKIES.get('email')
        conf_ca_emails = conference_dao.get_a_conference_ca_emails(name)
        if cur_user_email not in conf_ca_emails:
            raise Exception(
                "Only Conference admins are allowed to update conference")
        form = ConferenceForm(instance=conf)
        return render(request, "update_conference.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        form = ConferenceForm(request.POST, instance=conf)
        if form.is_valid():
            conference = form.save(commit=True)
            ca_emails = request.POST.get('ca_emails')
            ca_emails = ca_emails.split()
            for ca_email in ca_emails:
                try:
                    other_ca = accounts_dao.obtain_user_by_email(ca_email)
                    conference.ca.add(other_ca)
                except accounts_models.User.DoesNotExist:
                    # TODO: handle this event by sending email to creator indicating that the email doesnt exist
                    pass
            conference.save()
            messages.success(request, 'Conference succesfully updated')
            return redirect(list_conferences)
        else:
            return render(request, "update_conference.html", {"is_logged_in": is_logged_in, "form": form})


def create_workshop(request):
    is_logged_in = utils.check_login(request)
    if request.method == "GET":
        form = WorkshopForm()
        return render(request, "create_workshop.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        form = WorkshopForm(request.POST)
        if form.is_valid():
            workshop = form.save(commit=False)
            # assigning parent conference of workshop
            conf = conference_dao.get_conference_by_name(
                request.POST['parent_conference_name'])
            workshop.parent_conference = conf
            ca_emails = request.POST.get('ca_emails')
            # adding creator's email to ca_emails
            creator_email = request.POST['created_by']
            ca_emails += f" {creator_email}"
            workshop.ca_emails = ca_emails
            workshop.save()
            ca_emails = ca_emails.split()
            for ca_email in ca_emails:
                try:
                    # TODO: add accounts_dao
                    other_ca = accounts_dao.obtain_user_by_email(ca_email)
                    workshop.ca.add(other_ca)
                except accounts_models.User.DoesNotExist:
                    # TODO: handle this event by sending email to creator indicating that the email doesnt exist
                    pass
            messages.success(request, 'Workshop succesfully created')
            return redirect(list_conferences)
        else:
            return render(request, "create_workshop.html", {"is_logged_in": is_logged_in, "form": form})
        # afterwards portal admin validates it and sets is_valid field accordingly


def update_workshop(request, name):
    is_logged_in = utils.check_login(request)
    conf = conference_dao.get_workshop_by_name(name)
    if request.method == "GET":
        cur_user_email = request.COOKIES.get('email')
        workshop_ca_emails = conference_dao.get_a_workshop_ca_emails(name)
        if cur_user_email not in workshop_ca_emails:
            raise Exception(
                "Only Conference admins are allowed to update workshop")
        form = WorkshopForm(instance=conf)
        return render(request, "update_workshop.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        form = WorkshopForm(request.POST, instance=conf)
        if form.is_valid():
            workshop = form.save(commit=True)
            ca_emails = request.POST.get('ca_emails')
            ca_emails = ca_emails.split()
            for ca_email in ca_emails:
                try:
                    other_ca = accounts_dao.obtain_user_by_email(ca_email)
                    workshop.ca.add(other_ca)
                except accounts_models.User.DoesNotExist:
                    # TODO: handle this event by sending email to creator indicating that the email doesnt exist
                    pass
            workshop.save()
            messages.success(request, 'Conference succesfully updated')
            return redirect(list_conferences)
        else:
            return render(request, "update_workshop.html", {"is_logged_in": is_logged_in, "form": form})


def conference_details(request, conf_name=None):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        context_dict = conference_dao.get_conference_details(conf_name)
        context_dict['is_logged_in'] = is_logged_in
        return render(request, "conf_details.html", context_dict)
    return redirect('/accounts/')
