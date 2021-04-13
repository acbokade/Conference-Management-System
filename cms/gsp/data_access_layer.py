from . import models


def get_all_paper_submissions():
    return models.objects.objects.all()


def get_paper_submission_by_title(title):
    return models.PaperSubmission.objects.get(title=title)


def get_all_author_response_submissions():
    return models.AuthorResponseSubmission.objects().all()


def get_all_cam_pos_submissions():
    return models.CamPosSubmission.objects.all()
