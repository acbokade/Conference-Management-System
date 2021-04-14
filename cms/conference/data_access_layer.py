from . import models


def get_all_conferences():
    return models.Conference.objects.all()


def get_all_workshops():
    return models.Workshop.objects.all()


def get_all_conferences_names():
    return set(models.Conference.objects.all().values_list('name', flat=True))


def get_conference_by_name(name):
    return models.Conference.objects.get(name=name)


def get_a_conference_ca_emails(name):
    conf = get_conference_by_name(name)
    ca_emails_string = conf.ca_emails
    return ca_emails_string.split()


def get_workshop_by_name(name):
    return models.Workshop.objects.get(name=name)


def get_a_workshop_ca_emails(name):
    workshop = get_workshop_by_name(name)
    ca_emails_string = workshop.ca_emails
    return ca_emails_string.split()


def get_conference_subject_areas(name):
    conf = models.Conference.objects.get(name=name)
    conf_subject_areas = conf.subject_areas
    return conf_subject_areas.split(',')


def get_conference_details(conf_name):

    query_set = models.Conference.objects.filter(name=conf_name)

    if len(query_set) == 0:
        return {
            'conference_found': False,
            'name': conf_name
        }

    conf = query_set[0]

    return {
        'conference_found': True,
        'name': conf.name,
        'description': conf.description,
        'short_name': conf.short_name,
        'location': conf.location,
        'ca_emails': conf.ca_emails,
        'start_date': conf.start_date,
        'paper_submission_deadline': conf.paper_submission_deadline,
        'review_submission_deadline': conf.review_submission_deadline,
        'cam_pos_submission_deadline': conf.cam_pos_submission_deadline,
        'end_date': conf.end_date,
        'logo': conf.logo,
        'conf_url': conf.url,
        'subject_areas': conf.subject_areas,
        'expected_submissions': conf.expected_submissions,
        'ACM_conference_confirmation': conf.ACM_conference_confirmation,
        'ca': conf.ca
    }
