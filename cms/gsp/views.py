import conference
from django.forms import ValidationError
from django.shortcuts import render, redirect
from accounts import utils as account_utils
from accounts import views as account_views
from conference import views as conference_views
from .models import PaperSubmission, AuthorResponseSubmission, CamPosSubmission
from .forms import PaperSubmissionForm, AuthorResponseSubmissionForm, CamPosSubmissionForm
from . import utils


# Create your views here.
def render_gsp(request, event_id=None):
    if request.method == 'POST':
        form = PaperSubmissionForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            paper_submission = form.save(commit=False)

            # write some sanity checks

            paper_submission.save()
            # print('form saved')
            return redirect(conference.views.list_conferences)
        else:
            raise ValidationError('Invalid form {}'.format(form))

    if request.method == 'GET':
        # print(request.method, form)
        context_dict = dict()
        conf_status = utils.get_conference_status(request)
        user_status = utils.get_user_status(request)
        context_dict.update(conf_status)
        user_status.update(user_status)

        context_dict['paper_submission_form'] = PaperSubmissionForm()
        context_dict['author_response_submission_form'] = AuthorResponseSubmissionForm()
        context_dict['cam_pos_submission_form'] = CamPosSubmissionForm()

        return render(request, "gsp.html", context_dict)


def existing_conf_submissions(request, conf_name):
    is_logged_in = account_utils.check_login(request)
    if not is_logged_in:
        return redirect(account_views.login)

    context_dict = utils.get_user_existing_submissions(request)
    return render(request, "existing_submissions.html", context_dict)