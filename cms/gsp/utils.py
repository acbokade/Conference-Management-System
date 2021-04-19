from . import data_access_layer as gsp_dal
from .models import PaperSubmission
from conference.models import Conference
from accounts import data_access_layer as accounts_dao


def get_conference_status(request):

    return {
        'paper_submission_active': True,
        'author_response_submission_active': True,
        'cam_pos_submission_active': True
    }


def get_user_status(request):
    return {
        'user': {
            'title': 'QWERTY',
            'abstract': 'ASDFGH'
        }
    }


def get_user_existing_submissions(email, conf_name):

    submissions_query = gsp_dal.get_paper_submission_email_conf_name(
        email, conf_name)
    # print(type(submissions_query), submissions_query)
    submissions = list()
    for submission in submissions_query:
        # print(submission.title, submission.main_author.name, submission.conference.name)
        submissions.append({
            'title': submission.title,
            'status': "Submitted"
        })

    return {
        "conf_name": conf_name,
        "submissions": submissions
    }

def check_has_edit_conf_rights(conf_name, email):

    try:
        queryset = Conference.objects.get(name=conf_name)
        # print(queryset.ca)
    except Conference.DoesNotExist:
        print('does not exist')
        return False

    ca_emails = [ca.email for ca in queryset.ca.all()]
    if email in ca_emails:
        return True
    print('not found in emails of conference ca')
    return False