from .models import PaperSubmission

def get_conference_status(request):
    
    return {
        'paper_submission_active': True,
        'author_response_submission_active': False,
        'cam_pos_submission_active': False
    }

def get_user_status(request):
    return {
        'user': {
            'title': 'QWERTY',
            'abstract': 'ASDFGH'
        }
    }

def get_user_existing_submissions(user, conf_name):

    # submissions = PaperSubmission.objects.filter(main_author__name__exact=user, 
    #     conference__name__exact=conf_name)
    submissions_query = PaperSubmission.objects.all()
    # main_author__name__exact=user
    # , conference__name__exact=conf_name
    submissions = list()
    for submission in submissions_query:
        submissions.append({
            'title': submission.title,
            'status': "Submitted"
        })

    return {
        "conf_name": conf_name,
        "submissions": submissions
    }