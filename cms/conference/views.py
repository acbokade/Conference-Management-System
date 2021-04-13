from django.shortcuts import render, redirect
from accounts import utils
from datetime import datetime
from . import models
from accounts import models as accounts_models
from gsp import models as gsp_models
from accounts import views as account_views
from .forms import ConferenceForm, WorkshopForm
from . import data_access_layer as conference_dao
from accounts import data_access_layer as accounts_dao
# from accounts import data_access_layer as accounts_dao


def list_conferences(request):
    is_logged_in = utils.check_login(request)
    confs = conference_dao.get_all_conferences()
    workshops = conference_dao.get_all_workshops()
    return render(request, "list_conferences.html", {"is_logged_in": is_logged_in, "confs": confs, "workshops": workshops})


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

            return redirect(list_conferences)
        else:
            return render(request, "create_conference.html", {"form": form})
        # afterwards portal admin validates it and sets is_valid field accordingly


def update_conference(request, name):
    is_logged_in = utils.check_login(request)
    if request.method == "GET":
        conf = conference_dao.get_conference_by_name(name)
        form = ConferenceForm(instance=conf)
        return render(request, "update_conference.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        form = ConferenceForm(request.POST)
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
            return redirect(list_conferences)
        else:
            return render(request, "create_workshop.html", {"is_logged_in": is_logged_in, "form": form})
        # afterwards portal admin validates it and sets is_valid field accordingly


def update_workshop(request, name):
    is_logged_in = utils.check_login(request)
    if request.method == "GET":
        conf = conference_dao.get_workshop_by_name(name)
        form = WorkshopForm(instance=conf)
        return render(request, "update_workshop.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        form = WorkshopForm(request.POST)
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
            return redirect(list_conferences)
        else:
            return render(request, "update_workshop.html", {"is_logged_in": is_logged_in, "form": form})
