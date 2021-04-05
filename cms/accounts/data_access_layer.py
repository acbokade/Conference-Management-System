from . import models


def obtain_user_by_email(email):
    return models.User.objects.get(email=email)
