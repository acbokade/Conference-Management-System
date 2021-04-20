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


def get_users_by_research_interest(subject_area):
    related_users = []
    all_users = models.User.objects.all()
    for user in all_users:
        user_research_profile = user.researchprofile_set.all()
        if len(user_research_profile):
            research_interests = (
                user_research_profile[0].research_interests).split(',')
            if subject_area in research_interests:
                related_users.append(user)
    return related_users
