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