from .models import Conference
from . import data_access_layer as conf_dao
from reviewer import models as reviewer_models


def get_subject_areas_list_by_conf_name(conf_name):
    conf = conf_dao.get_conference_by_name(conf_name)
    subject_areas = conf.subject_areas
    subject_areas_list = subject_areas.split(',')
    return subject_areas_list


def obtain_ca_boolean_array(user_email, confs_list):
    arr = []
    for conf in confs_list:
        conf_ca_list = [em.strip() for em in conf.ca_emails.split(' ')]
        if user_email.strip() in conf_ca_list:
            arr.append(True)
        else:
            arr.append(False)
    return arr


def obtain_invited_rev_boolean_array(user_email, confs_list):
    arr = []
    for conf in confs_list:
        try:
            reviewer_models.InvitedReviewers.objects.get(
                user=user_email, conference=conf)
            arr.append(True)
        except:
            arr.append(False)
    return arr
