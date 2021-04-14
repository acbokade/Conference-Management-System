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


def get_all_workshops():
    return models.Workshop.objects.all()


def get_workshop_by_name(name):
    return models.Workshop.objects.get(name=name)


def get_a_workshop_ca_emails(name):
    workshop = get_workshop_by_name(name)
    ca_emails_string = workshop.ca_emails
    return ca_emails_string.split()
