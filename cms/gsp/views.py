import conference
from django.forms import ValidationError
from django.shortcuts import render, redirect
from accounts import utils as account_utils
from accounts import views as account_views
from accounts import data_access_layer as accounts_dal
from conference import data_access_layer as conference_dal
from . import data_access_layer as gsp_dal
from conference import views as conference_views
from .models import PaperSubmission, AuthorResponseSubmission, CamPosSubmission
from .forms import PaperSubmissionForm, AuthorResponseSubmissionForm, CamPosSubmissionForm
from django.contrib import messages
from . import utils

# Create your views here.

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


def render_gsp(request, conf_name):
    is_logged_in = account_utils.check_login(request)
    if not is_logged_in:
        return redirect('/accounts/login')
    if request.method == 'POST':
        form = PaperSubmissionForm(request.POST, request.FILES)
        email = request.COOKIES.get('email')

        if form.is_valid():
            paper_submission = form.save(commit=False)
            paper_submission.main_author = accounts_dal.obtain_user_by_email(
                email)
            paper_submission.conference = conference_dal.get_conference_by_name(
                conf_name)
            # write some sanity checks

            paper_submission.save()
            # print('form saved')
            return redirect(f'/gsp/{conf_name}/existing_conf_submissions')
        else:
            paper_submission = form.save(commit=False)
            paper_submission.main_author = accounts_dal.obtain_user_by_email(
                email)
            paper_submission.conference = conference_dal.get_conference_by_name(
                conf_name)
            existing_submission = gsp_dal.get_paper_submission(
                email, conf_name, paper_title)
            print('existing submissions', existing_submission)
            if existing_submission is None:
                print('no similar submission found')
                return redirect(f'/gsp/{conf_name}/new_submission')
            else:
                print('submission exists')
                existing_submission.update(form)
                return redirect(f'/gsp/{conf_name}/existing_conf_submissions')
            print('form invalid', form.errors)
    else:
        conf = conference_dal.get_conference_by_name(conf_name)
        conf_subject_areas = conf.subject_areas.split(',')
        context_dict = dict()
        context_dict.update({"is_logged_in": is_logged_in})
        conf_status = utils.get_conference_status(request)
        user_status = utils.get_user_status(request)
        context_dict.update(conf_status)
        user_status.update(user_status)

        context_dict['paper_submission_form'] = PaperSubmissionForm(
            conf_subject_areas=conf_subject_areas)
        context_dict['author_response_submission_form'] = AuthorResponseSubmissionForm()
        context_dict['cam_pos_submission_form'] = CamPosSubmissionForm()

        return render(request, "gsp.html", context_dict)


def existing_conf_submissions(request, conf_name):
    is_logged_in = account_utils.check_login(request)
    if not is_logged_in:
        return redirect(account_views.login)
    has_edit_conf_rights = utils.check_has_edit_conf_rights(conf_name, request.COOKIES.get('email'))
    context_dict = utils.get_user_existing_submissions(
        request.COOKIES.get('email'), conf_name)
    context_dict.update({"is_logged_in": is_logged_in})
    context_dict['has_edit_conf_rights'] = has_edit_conf_rights
    return render(request, "existing_submissions.html", context_dict)


def edit_submission(request, conf_name=None, paper_title=None):
    is_logged_in = account_utils.check_login(request)
    email = request.COOKIES.get('email')
    query_set = gsp_dal.get_paper_submission(email, conf_name, paper_title)
    if request.method == 'GET':
        if query_set is not None:
            pass

            context_dict = dict()
            context_dict.update({"is_logged_in": is_logged_in})
            conf_status = utils.get_conference_status(request)
            user_status = utils.get_user_status(request)
            context_dict.update(conf_status)
            context_dict.update(user_status)

            context_dict['paper_submission_form'] = PaperSubmissionForm(
                instance=query_set)

            return render(request, "gsp.html", context_dict)
        else:
            return redirect(f'/gsp/{{ conf_name }}/existing_conf_submissions')
    elif request.method == 'POST':
        form = PaperSubmissionForm(request.POST, request.FILES)

        email = request.COOKIES.get('email')

        if form.is_valid():
            paper_submission = form.save(commit=False)
            paper_submission.main_author = accounts_dal.obtain_user_by_email(
                email)
            paper_submission.conference = conference_dal.get_conference_by_name(
                conf_name)
            # write some sanity checks

            paper_submission.save()
            # print('form saved')
            # return redirect(f'/gsp/{conf_name}/existing_conf_submissions')
        print('form invalid', form.errors)
        return redirect(f'/gsp/{conf_name}/existing_conf_submissions')


def withdraw_submission(request, conf_name=None, paper_title=None):
    is_logged_in = account_utils.check_login(request)
    email = request.COOKIES.get('email')
    gsp_dal.delete_paper_submission(email, conf_name, paper_title)

    return redirect(f'/gsp/{conf_name}/existing_conf_submissions')
    # context_dict = utils.get_user_existing_submissions(request.user, conf_name)
    # return render(request, "existing_submissions.html", context_dict)
