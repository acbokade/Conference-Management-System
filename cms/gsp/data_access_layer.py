from . import models
from conference import data_access_layer as conference_dao


def get_all_paper_submissions():
    return models.objects.objects.all()


def get_all_paper_submissions_of_conf(conf_name):
    conf = conference_dao.get_conference_by_name(conf_name)
    return list(conf.papersubmission_set.all())


def get_paper_submission_by_title(title):
    return models.PaperSubmission.objects.get(title=title)


def get_all_author_response_submissions():
    return models.AuthorResponseSubmission.objects().all()


def get_all_cam_pos_submissions():
    return models.CamPosSubmission.objects.all()


def delete_paper_submission(email, conf_name, paper_title):
    try:
        query_set = models.PaperSubmission.objects.get(
            main_author__email=email,
            conference__name=conf_name,
            title=paper_title
        )
        query_set.delete()
    except models.PaperSubmission.DoesNotExist:
        pass


def get_paper_submission_email_conf_name(email, conf_name):

    query_set = models.PaperSubmission.objects.get(
        main_author__email=email,
        conference__name=conf_name
    )

    return query_set


def get_paper_submission(email, conf_name, paper_title):

    try:
        query_set = models.PaperSubmission.objects.get(
            main_author__email=email,
            conference__name=conf_name,
            title=paper_title
        )
        return query_set
    except models.PaperSubmission.DoesNotExist:
        return None
