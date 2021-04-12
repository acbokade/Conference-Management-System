from django.shortcuts import render

from .forms import PaperSubmissionForm, AuthorResponseSubmissionForm, CamPosSubmissionForm
from . import utils

# Create your views here.
def render_gsp(request, event_id=None):

    # if request.method == 'POST':
    context_dict = dict()
    conf_status = utils.get_conference_status(request)
    user_status = utils.get_user_status(request)
    context_dict.update(conf_status)
    user_status.update(user_status)

    context_dict['paper_submission_form'] = PaperSubmissionForm()
    context_dict['author_response_submission_form'] = AuthorResponseSubmissionForm()
    context_dict['cam_pos_submission_form'] = CamPosSubmissionForm()

    return render(request, "gsp.html", context_dict)