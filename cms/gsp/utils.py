from . import data_access_layer as gsp_dal 

from .models import PaperSubmission

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

    submissions_query = gsp_dal.get_paper_submission_email_conf_name(email, conf_name)

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
