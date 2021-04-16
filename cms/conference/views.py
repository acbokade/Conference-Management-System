from django.shortcuts import render, redirect
from django.contrib import messages
from accounts import utils
from datetime import datetime
from . import models
from accounts import models as accounts_models
from gsp import models as gsp_models
from accounts import views as account_views
from . import data_access_layer as conference_dao
from accounts import data_access_layer as accounts_dao
from .forms import ConferenceForm
from . import utils as conf_utils
from django.utils import timezone
from .constants import CONF_UPDATE_DEADLINE
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
        is_ca_confs = conf_utils.obtain_ca_boolean_array(
            request.COOKIES.get('email'), confs)
        is_invited_as_revs = conf_utils.obtain_invited_rev_boolean_array(
            request.COOKIES.get('email'), confs)
        assert len(confs) == len(is_ca_confs) == len(is_invited_as_revs)

        confs_list = zip(confs, is_ca_confs, is_invited_as_revs)
        return render(request, "list_conferences.html", {"is_logged_in": is_logged_in, "confs_list": confs_list})
    return redirect('/accounts/')


def list_my_conferences(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        author = accounts_dao.obtain_user_by_email(
            request.COOKIES.get('email'))
        conf_submissions = gsp_models.PaperSubmission.objects.all().filter(main_author=author)
        confs = [subm.conference for subm in conf_submissions]

        # Write code to obtain workshop submission
        # workshops = gsp_models.PaperSubmission.objects.get(main_author=author)

        return render(request, "list_my_conferences.html", {"is_logged_in": is_logged_in,
                                                            "confs": confs})
    return redirect('/accounts/')


def create_conference(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        if request.method == "POST":
            form = ConferenceForm(request.POST, request.FILES)
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
            return render(request, "create_conference.html", {"form": form})
            # afterwards portal admin validates it and sets is_valid field accordingly
        else:
            form = ConferenceForm()
        return render(request, "create_conference.html", {"is_logged_in": is_logged_in, "form": form})
    return redirect('/accounts/')


def update_conference(request, name):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        conf = conference_dao.get_conference_by_name(name)
        # checking if deadline to update conference isn't elapsed
        current_time = timezone.now()
        if (current_time - conf.created_at).days > CONF_UPDATE_DEADLINE:
            messages.error(
                request, f"Sorry, Not allowed to update conference after {CONF_UPDATE_DEADLINE} days")
            redirect(list_conferences)
        # checking if user is CA of the conference
        cur_user_email = request.COOKIES.get('email')
        conf_ca_emails = conference_dao.get_a_conference_ca_emails(name)
        if cur_user_email not in conf_ca_emails:
            messages.error(
                request, f"Only Conference admins are allowed to update conference")
            redirect(list_conferences)
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
            return render(request, "update_conference.html", {"is_logged_in": is_logged_in, "form": form})
        else:
            form = ConferenceForm(instance=conf)
        return render(request, "update_conference.html", {"is_logged_in": is_logged_in, "form": form})
    return redirect('/accounts/')


def conference_details(request, conf_name=None):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        context_dict = conference_dao.get_conference_details(conf_name)
        context_dict['is_logged_in'] = is_logged_in
        return render(request, "conf_details.html", context_dict)
    return redirect('/accounts/')
