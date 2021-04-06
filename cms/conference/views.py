from django.shortcuts import render, redirect
from accounts import utils
from datetime import datetime
from . import models
from accounts import models as accounts_models
from .forms import ConferenceForm


def list_conferences(request):
    is_logged_in = utils.check_login(request)
    confs = models.Conference.objects.all()
    return render(request, "list_conferences.html", {"is_logged_in": is_logged_in, "confs": confs})


def create_conference(request):
    is_logged_in = utils.check_login(request)
    if request.method == "GET":
        form = ConferenceForm()
        return render(request, "create_conference.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        form = ConferenceForm(request.POST)
        if form.is_valid():
            conference = form.save(commit=False)
            conference.save()
            ca_emails = request.POST.get('ca_emails')
            for ca_email in ca_emails:
                try:
                    other_ca = accounts_models.User.objects.get(email=ca_email)
                    conference.ca.add(other_ca)
                except accounts_models.User.DoesNotExist:
                    # TODO: handle this event by sending email to creator indicating that the email doesnt exist
                    pass
            confs = models.Conference.objects.all()
            return redirect(list_conferences)
        else:
            return render(request, "create_conference.html", {"form": form})
        # afterwards portal admin validates it and sets is_valid field accordingly


def update_conference(request, name):
    is_logged_in = utils.check_login(request)
    if request.method == "GET":
        conf = models.Conference.objects.get(name=name)
        form = ConferenceForm(instance=conf)
        return render(request, "update_conference.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        form = ConferenceForm(request.POST)
        if form.is_valid():
            conference = form.save(commit=False)
            conference.save()
            ca_emails = request.POST.get('ca_emails')
            for ca_email in ca_emails:
                if ca_email in conference.ca_emails:
                    continue
                try:
                    other_ca = accounts_models.User.objects.get(email=ca_email)
                    conference.ca.add(other_ca)
                except accounts_models.User.DoesNotExist:
                    # TODO: handle this event by sending email to creator indicating that the email doesnt exist
                    pass
            confs = models.Conference.objects.all()
            return redirect(list_conferences)
        else:
            return render(request, "update_conference.html", {"is_logged_in": is_logged_in, "form": form})


def create_workshop(request):
    pass
