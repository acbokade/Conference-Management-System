from . import models


def obtain_user_by_email(email):
    return models.User.objects.get(email=email)


def obtain_research_profile(email):
    return models.ResearchProfile.objects.get(person=obtain_user_by_email(email))


def get_user_by_username(name):
    return models.User.objects.get(name=name)


def obtain_user_security_question(email):
    return models.SecurityQuestions.objects.get(user=obtain_user_by_email(email)).question


def obtain_user_security_answer(email):
    return models.SecurityQuestions.objects.get(user=obtain_user_by_email(email)).answer
