from .models import Conference
from . import data_access_layer as conf_dao


def get_subject_areas_list_by_conf_name(conf_name):
    conf = conf_dao.get_conference_by_name(conf_name)
    subject_areas = conf.subject_areas
    subject_areas_list = subject_areas.split(',')
    return subject_areas_list
