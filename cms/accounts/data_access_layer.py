from . import models


def obtain_user_by_email(email):
    return models.User.objects.get(email=email)


def obtain_research_profile(email):
    return models.ResearchProfile.objects.get(person=obtain_user_by_email(email))

def get_user_by_username(uname):
    return models.User.objects.get(name=name)